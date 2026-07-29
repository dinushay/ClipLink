## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.

## 2024-07-29 - Visual Affordances in Discord Embeds
**Learning:** Raw seconds in duration and plain text buttons lack scannability. Adding emojis (`⏱️`, `🎬`, `📼`) and formatting times to `MM:SS` significantly improves the quick readability of Discord bot embeds.
**Action:** When creating or modifying embeds, consider converting raw data into formatted human-readable strings and use emojis as visual affordances for action buttons.
