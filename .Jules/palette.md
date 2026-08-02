## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.

## 2024-05-24 - Async Loading States
**Learning:** Users often experience timeouts or perceived unresponsiveness when slash commands make external API calls. Providing a deferred loading state drastically improves UX by signaling that the bot is processing the request.
**Action:** Used `await interaction.response.defer(ephemeral=True)` and `interaction.send()` in async slash commands that fetch data to provide immediate feedback.
