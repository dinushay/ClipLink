## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.

## 2026-07-31 - Better loading state for Async API commands
**Learning:** Nextcord slash commands have a strict 3-second limit to respond, which causes the command to fail/timeout when fetching external APIs (like Twitch).
**Action:** Use `await interaction.response.defer(ephemeral=True)` immediately inside the command to provide users with a "Bot is thinking..." state. Then, use `await interaction.send()` to respond. This provides much better feedback during long-running tasks.
