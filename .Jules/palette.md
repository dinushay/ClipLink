## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.
## 2024-05-18 - Add Icons to Discord UI Buttons
**Learning:** Text-only link buttons in Discord integrations can lack visual hierarchy and blend together. Adding relevant emojis to `nextcord.ui.Button` elements acts as a visual cue, improving scannability and cognitive accessibility for users navigating rich embeds.
**Action:** Consistently use emojis alongside text labels in interactive Discord components (like buttons and menus) to clarify their function and provide immediate visual context.
