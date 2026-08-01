## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.
## 2026-08-01 - Loading States for Async Commands
**Learning:** External API calls in Discord slash commands can cause 3-second timeouts resulting in a jarring "The application did not respond" error. Deferring the response immediately provides a "Bot is thinking..." loading state, vastly improving perceived performance and preventing timeouts.
**Action:** Added `await interaction.response.defer(ephemeral=True)` at the start of async slash commands and replaced `interaction.response.send_message` with `interaction.send()`.
