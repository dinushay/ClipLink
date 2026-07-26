## 2026-07-25 - Forgiving Inputs for URLs
**Learning:** Users often copy and paste full URLs instead of just usernames or IDs, leading to frustrating validation errors if the input is strictly validated against the username format. By adding a bit of parsing logic to gracefully handle URLs, we can drastically improve the UX and reduce friction.
**Action:** Implemented a URL parser in the `/addstreamer` command that extracts the username if a full Twitch URL is pasted, allowing for more forgiving inputs without changing the core functionality.

## 2024-05-24 - Actionable Bot Error Messages
**Learning:** Pure error messages without next steps can leave users feeling stuck, particularly in a conversational UI like Discord. Users need actionable guidance to recover gracefully from a command failure.
**Action:** Always include a helpful '💡 Tip:' with actionable next steps (like alternative commands, spell checking, or checking permissions) alongside the failure reason when presenting errors back to the user.
