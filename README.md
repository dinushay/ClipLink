# ClipLink

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

**ClipLink** is a powerful and easy-to-use Discord bot designed to automatically fetch and post the latest Twitch clips from your favorite streamers directly into your Discord server. Keep your community updated with the best moments as they happen!

This bot is the code behind the [ClipLink Discord Bot](https://discord.com/oauth2/authorize?client_id=990591720653729842&scope=bot&permissions=19456).


---

## ✨ Features

- **Automatic Clip Fetching**: The bot periodically checks for new clips from your chosen streamers.
- **Instant Notifications**: As soon as a new clip is found, it's posted in a designated channel.
- **Rich Embeds**: Clips are presented in a clean, informative embed, including the clip title, creator, game category, and a direct link.
- **VOD Linking**: Includes a button to jump directly to the moment in the VOD where the clip was created (if available).
- **User-Friendly Commands**: Simple and intuitive slash commands for adding, listing, and removing streamers.
- **Autocomplete Support**: Easily find the streamer you want to remove with smart autocompletion.

---

## 🚀 Installation

To host your own instance of ClipLink, follow these steps.

### Prerequisites

- Python 3.8 or newer
- A Discord Bot Token ([Discord Developer Portal](https://discord.com/developers/applications))
- Twitch API Token (Client ID, Access Token, Refresh Token) ([twitchtokengenerator.com](https://twitchtokengenerator.com/))

### Setup Steps

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/dinushay/ClipLink.git
    cd ClipLink
    ```

2.  **Install the required libraries:**
    ```sh
    pip install nextcord aiohttp
    ```

3.  **Create the configuration file:**
    Create a file named `config.json` in the main directory and add your credentials.

    ```json
    {
        "DISCORD_BOT_TOKEN": "YOUR_DISCORD_BOT_TOKEN_HERE",
        "TWITCH_CLIENT_ID": "YOUR_TWITCH_CLIENT_ID_HERE",
        "TWITCH_ACCESS_TOKEN": "YOUR_TWITCH_OAUTH_ACCESS_TOKEN_HERE",
        "TWITCH_REFRESH_TOKEN": "YOUR_TWITCH_REFRESH_TOKEN_HERE"
    }
    ```

4.  **Run the bot:**
    ```sh
    python clip.py
    ```

---

## ⚙️ Configuration

The bot's behavior can be adjusted through the global variables at the top of the `clip.py` file:

-   `CONFIG_FILE`: The name of the configuration file (default: `"config.json"`).
-   `DATA_FILE`: The name of the database file where streamer information is stored (default: `"database.json"`).
-   `CHECK_INTERVAL_SECONDS`: How often (in seconds) the bot checks for new clips (default: `60`).
-   `MAX_STREAMERS_PER_GUILD`: The maximum number of streamers that can be added to one Discord server (default: `5`).
-   `DEBUG_MODE`: Set to `True` for detailed logging in the console (default: `Frue`).

---

## 🤖 Usage

ClipLink uses intuitive slash commands. Only users with the `Manage Channels` permission can use these commands.

### `/addstreamer`
Adds a Twitch streamer to the monitoring list.

-   **`twitch_user`**: The Twitch username or user ID of the streamer.
-   **`channel`** (Optional): The Discord channel where clip notifications will be sent. If not specified, the channel where the command is used will be chosen.

**Example:**
`/addstreamer twitch_user:shroud channel:#clips`

### `/liststreamers`
Lists all the streamers currently being monitored on the server.

**Example:**
`/liststreamers`

### `/removestreamer`
Removes a streamer from the monitoring list.

-   **`streamer`**: The ID of the streamer to remove. This field supports autocomplete to help you find the right one.

**Example:**
`/removestreamer streamer:12345678`

---

## 🔐 Permissions

For the bot to function correctly, it needs the following permissions:

-   **View Channel**: To see the designated clips channel.
-   **Send Messages**: To post clip notifications in the channel.
-   **Embed Links**: To properly display the rich embeds for clips.

Users need the `Manage Channels` permission in your server to be able to add or remove streamers.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
