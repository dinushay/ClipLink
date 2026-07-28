## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.
## 2026-07-28 - [Discord Bot Buttons Enhancement]
**Learning:** In text-heavy environments like Discord, simple emojis significantly improve scannability and action recognition on UI components like buttons.
**Action:** When creating or updating interactive components (like nextcord.ui.Button), try to include relevant emojis to serve as visual anchors for the user.
