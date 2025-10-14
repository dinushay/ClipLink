import nextcord
from nextcord.ext import commands, tasks
import json
import os
import aiohttp
from datetime import datetime, timedelta, timezone

# =============================
#  Configuration & Global Variables
# =============================

CONFIG_FILE = "config.json"
DATA_FILE = "database.json"
CHECK_INTERVAL_SECONDS = 60
MAX_STREAMERS_PER_GUILD = 5
DEBUG_MODE = False

# Load configuration
try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    DISCORD_BOT_TOKEN = config["DISCORD_BOT_TOKEN"]
    TWITCH_CLIENT_ID = config["TWITCH_CLIENT_ID"]
    TWITCH_ACCESS_TOKEN = config["TWITCH_ACCESS_TOKEN"]
    TWITCH_REFRESH_TOKEN = config["TWITCH_REFRESH_TOKEN"]
except FileNotFoundError:
    print("[FATAL] config.json not found. Please create the file and add your tokens.")
    exit()
except KeyError as e:
    print(f"[FATAL] Missing key in config.json: {e}")
    exit()

# Bot instance
intents = nextcord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(intents=intents)

# =============================
#  Data Management (JSON)
# =============================

def load_data():
    """Loads the streamer configuration from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    """Saves the streamer configuration to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =============================
#  Twitch API Helpers
# =============================

async def refresh_twitch_token():
    """Refreshes the Twitch access token."""
    global TWITCH_ACCESS_TOKEN
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": TWITCH_CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": TWITCH_REFRESH_TOKEN,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                TWITCH_ACCESS_TOKEN = data["access_token"]
                if DEBUG_MODE:
                    print("[INFO] Twitch access token refreshed.")
                return True
            else:
                if DEBUG_MODE:
                    print(f"[ERROR] Token refresh failed. Status: {resp.status}, Response: {await resp.text()}")
                return False

async def get_twitch_user(identifier):
    """Fetches Twitch user data by name or ID."""
    headers = {
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
        "Client-Id": TWITCH_CLIENT_ID,
    }
    param_type = "login" if not identifier.isdigit() else "id"
    url = f"https://api.twitch.tv/helix/users?{param_type}={identifier}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 401:
                if DEBUG_MODE:
                    print("[INFO] Token expired. Attempting refresh...")
                if await refresh_twitch_token():
                    return await get_twitch_user(identifier)
                return None

            if resp.status == 200:
                data = await resp.json()
                if data.get("data"):
                    return data["data"][0]
    return None

async def get_twitch_game(game_id):
    """Fetches Twitch game data by ID."""
    if not game_id:
        return "N/A"
    headers = {
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
        "Client-Id": TWITCH_CLIENT_ID,
    }
    url = f"https://api.twitch.tv/helix/games?id={game_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 401:
                if await refresh_twitch_token():
                    return await get_twitch_game(game_id)
                return "N/A"

            if resp.status == 200:
                data = await resp.json()
                if data.get("data"):
                    return data["data"][0]["name"]
    return "N/A"

async def get_latest_clip(broadcaster_id):
    """Fetches the latest clip for a broadcaster within the last day."""
    headers = {
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
        "Client-Id": TWITCH_CLIENT_ID,
    }
    started_at = (datetime.now(timezone.utc) - timedelta(seconds=CHECK_INTERVAL_SECONDS + 5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}&first=1&started_at={started_at}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 401:
                if await refresh_twitch_token():
                    return await get_latest_clip(broadcaster_id)
                return None

            if resp.status == 200:
                data = await resp.json()
                return data["data"][0] if data.get("data") else None
    return None

# =============================
#  Bot Events and Background Task
# =============================

@bot.event
async def on_ready():
    print(f"[INFO] Bot is logged in as: {bot.user}")
    activity = nextcord.Streaming(name="🔗 dinushay.de", url="https://www.twitch.tv/dinu_shay")
    await bot.change_presence(activity=activity)
    clip_checker.start()

@tasks.loop(seconds=CHECK_INTERVAL_SECONDS)
async def clip_checker():
    if not bot.is_ready():
        return

    all_streamers = load_data()
    if not all_streamers:
        return

    if DEBUG_MODE and all_streamers:
        print(f"[DEBUG] Checking {len(all_streamers)} streamer(s)...")

    updated_streamers = []
    streamers_to_remove = []

    for entry in all_streamers:
        guild = bot.get_guild(entry["server_id"])
        streamer_id = entry["streamer_id"]

        if not guild:
            streamers_to_remove.append(entry)
            if DEBUG_MODE:
                print(f"[CLEANUP] Bot no longer on server {entry['server_id']}. Removing entry for {streamer_id}.")
            try:
                user = await bot.fetch_user(entry["added_by_user_id"])
                twitch_user_info = await get_twitch_user(streamer_id)
                streamer_display_name = twitch_user_info['display_name'] if twitch_user_info else streamer_id
                await user.send(f"Hey! The bot was removed from the server where you added the streamer **{streamer_display_name}** (`{streamer_id}`). Your notification has therefore been deleted.")
            except (nextcord.NotFound, nextcord.Forbidden):
                pass
            continue

        channel = guild.get_channel(entry["channel_id"])

        if not channel or not channel.permissions_for(guild.me).view_channel or not channel.permissions_for(guild.me).send_messages or not channel.permissions_for(guild.me).embed_links:
            streamers_to_remove.append(entry)
            if DEBUG_MODE:
                print(f"[CLEANUP] Channel {entry['channel_id']} not found or permissions missing on server {guild.name}. Removing entry.")
            try:
                user = await bot.fetch_user(entry["added_by_user_id"])
                twitch_user_info = await get_twitch_user(streamer_id)
                streamer_display_name = twitch_user_info['display_name'] if twitch_user_info else streamer_id
                await user.send(f"Hey! The channel for clip notifications from streamer **{streamer_display_name}** (`{streamer_id}`) on the server `{guild.name}` is no longer accessible (deleted or missing permissions [`Embed Links`, `Send Messages` and `View Channels`]). The notification has been removed.")
            except (nextcord.NotFound, nextcord.Forbidden):
                pass
            continue

        clip = await get_latest_clip(streamer_id)

        if clip is None and entry.get("last_clip_id") is None:
            if DEBUG_MODE:
                print(f"[DEBUG] No clips found yet for streamer {streamer_id}. Will check again.")

        elif clip and clip["id"] != entry.get("last_clip_id"):
            if DEBUG_MODE:
                print(f"[NEW CLIP] New clip found for {clip['broadcaster_name']} ({clip['broadcaster_id']}): {clip['id']}")
            entry["last_clip_id"] = clip["id"]

            game_name = await get_twitch_game(clip.get("game_id", ""))
            dt_object = datetime.fromisoformat(clip['created_at'].replace('Z', '+00:00'))
            timestamp = int(dt_object.timestamp())

            embed = nextcord.Embed(
                title=f"🎬｜New Clip at {clip['broadcaster_name']}",
                description=f"**[{clip['title']}]({clip['url']})**",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="Created by", value=clip['creator_name'], inline=True)
            embed.add_field(name="Category", value=game_name, inline=True)
            embed.add_field(name="Created", value=f"<t:{timestamp}:R>", inline=True)
            embed.set_image(url=clip['thumbnail_url'])
            embed.set_footer(text=f"Duration: {int(clip['duration'])} seconds")

            view = nextcord.ui.View()
            view.add_item(nextcord.ui.Button(label="View Clip", style=nextcord.ButtonStyle.link, url=clip['url']))

            if clip.get("video_id") and clip.get("vod_offset") is not None:
                video_id = clip["video_id"]
                offset = clip["vod_offset"]
                
                hours = offset // 3600
                minutes = (offset % 3600) // 60
                seconds = offset % 60
                vod_timestamp = f"{hours}h{minutes}m{seconds}s"
                
                vod_url = f"https://www.twitch.tv/videos/{video_id}?t={vod_timestamp}"
                
                view.add_item(nextcord.ui.Button(label="Go to VOD", style=nextcord.ButtonStyle.link, url=vod_url))
            
            try:
                await channel.send(embed=embed, view=view)
            except nextcord.Forbidden:
                if DEBUG_MODE:
                    print(f"[ERROR] No permission to send in channel {channel.id} on server {guild.name}.")

        updated_streamers.append(entry)

    final_data = [e for e in updated_streamers if e not in streamers_to_remove]
    save_data(final_data)

@clip_checker.before_loop
async def before_checker():
    await bot.wait_until_ready()

# =============================
#  Slash Commands
# =============================

@bot.slash_command(
    description="Adds a Twitch streamer for clip notifications.",
    default_member_permissions=nextcord.Permissions(manage_channels=True)
)
async def addstreamer(
    interaction: nextcord.Interaction,
    twitch_user: str = nextcord.SlashOption(description="The name or ID of the Twitch streamer.", required=True),
    channel: nextcord.abc.GuildChannel = nextcord.SlashOption(
        description="The Discord channel to send clips to (optional).",
        required=False,
        channel_types=[nextcord.ChannelType.text]
    )
):
    target_channel = channel or interaction.channel

    if not target_channel.permissions_for(interaction.guild.me).view_channel or \
       not target_channel.permissions_for(interaction.guild.me).send_messages or \
       not target_channel.permissions_for(interaction.guild.me).embed_links:
        await interaction.response.send_message(
            "❌ **Error:** I need the `View Channel`, `Send Messages`, and `Embed Links` permissions in the selected channel to function.",
            ephemeral=True
        )
        return

    all_data = load_data()
    guild_data = [s for s in all_data if s["server_id"] == interaction.guild.id]

    if len(guild_data) >= MAX_STREAMERS_PER_GUILD:
        await interaction.response.send_message(
            f"❌ **Error:** The limit of **{MAX_STREAMERS_PER_GUILD}** streamers per server has been reached.",
            ephemeral=True
        )
        return

    twitch_account = await get_twitch_user(twitch_user)
    if not twitch_account:
        await interaction.response.send_message(
            f"❌ **Error:** A Twitch channel with the name/ID `{twitch_user}` could not be found.",
            ephemeral=True
        )
        return

    streamer_id = twitch_account["id"]
    streamer_name = twitch_account["display_name"]

    if any(s["streamer_id"] == streamer_id for s in guild_data):
        await interaction.response.send_message(
            f"❌ **Error:** The streamer **{streamer_name}** is already being monitored on this server.",
            ephemeral=True
        )
        return

    new_entry = {
        "streamer_id": streamer_id,
        "server_id": interaction.guild.id,
        "channel_id": target_channel.id,
        "added_by_user_id": interaction.user.id,
        "last_clip_id": None
    }
    all_data.append(new_entry)
    save_data(all_data)

    await interaction.response.send_message(
        f"✅ **Success!** The streamer **{streamer_name}** is now being monitored. New clips will be posted in {target_channel.mention}.",
        ephemeral=True
    )

@bot.slash_command(description="Lists all monitored streamers on this server.")
async def liststreamers(interaction: nextcord.Interaction):
    guild_data = [s for s in load_data() if s["server_id"] == interaction.guild.id]

    if not guild_data:
        await interaction.response.send_message("ℹ️ No streamers are currently being monitored on this server.", ephemeral=True)
        return

    embed = nextcord.Embed(
        title=f"Monitored streamers on {interaction.guild.name}",
        color=nextcord.Color.blue()
    )

    for entry in guild_data:
        twitch_user = await get_twitch_user(entry["streamer_id"])
        streamer_name = twitch_user["display_name"] if twitch_user else "Unknown Streamer"

        channel = interaction.guild.get_channel(entry["channel_id"])
        channel_mention = channel.mention if channel else "Channel not found"

        embed.add_field(
            name=f"{streamer_name} ({entry['streamer_id']})",
            value=f"Added by: <@{entry['added_by_user_id']}>\nChannel: {channel_mention}",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(
    description="Removes a streamer from the monitoring list.",
    default_member_permissions=nextcord.Permissions(manage_channels=True)
)
async def removestreamer(
    interaction: nextcord.Interaction,
    streamer: str = nextcord.SlashOption(description="The ID of the streamer to remove.", required=True)
):
    all_data = load_data()

    entry_to_remove = None
    for entry in all_data:
        if entry["server_id"] == interaction.guild.id and entry["streamer_id"] == streamer:
            entry_to_remove = entry
            break

    if not entry_to_remove:
        await interaction.response.send_message("❌ **Error:** A streamer with this ID is not being monitored on this server.", ephemeral=True)
        return

    all_data.remove(entry_to_remove)
    save_data(all_data)

    await interaction.response.send_message(f"✅ **Success!** The streamer with the ID `{streamer}` is no longer being monitored.", ephemeral=True)

@removestreamer.on_autocomplete("streamer")
async def streamer_autocomplete(interaction: nextcord.Interaction, streamer: str):
    guild_data = [s for s in load_data() if s["server_id"] == interaction.guild.id]
    choices = {}
    
    for entry in guild_data:
        user_info = await get_twitch_user(entry["streamer_id"])
        name = user_info["display_name"] if user_info else f"ID: {entry['streamer_id']}"
        if streamer.lower() in name.lower():
            choices[f"{name} ({entry['streamer_id']})"] = entry['streamer_id']

    await interaction.response.send_autocomplete(choices)

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error: Exception):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            "❌ **Error:** You do not have the required permission (`Manage Channels`) to execute this command.",
            ephemeral=True
        )
    else:
        if DEBUG_MODE:
            print(f"[COMMAND ERROR] An error occurred: {error}")
        try:
            await interaction.response.send_message(
                "An unexpected error occurred. Please try again later.",
                ephemeral=True
            )
        except nextcord.errors.InteractionResponded:
            pass

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
