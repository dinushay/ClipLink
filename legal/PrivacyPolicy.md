## Privacy Policy

_Last Updated: October 15, 2025_

This Privacy Policy explains what information the Clip Notifier Bot ("ClipLink") collects, why it is collected, and how it is used and stored. By using the Bot, you consent to the data practices described in this policy.

### 1. Information We Collect

The Bot is designed to be minimal in its data collection. We only store data that is essential for its operation. The following data is stored in our database:

- **Discord Server ID:** The ID of the Discord server where the Bot is configured. This is necessary to associate monitored streamers with the correct server.
- **Discord Channel ID:** The ID of the channel designated for clip notifications. This tells the Bot where to send messages.
- **Discord User ID:** The ID of the user who adds a streamer for monitoring. This is stored to provide context on who configured the notification and to allow for potential direct message notifications in case of a configuration error (e.g., the bot is removed from the server or loses channel permissions).
- **Twitch Streamer ID:** The numerical ID of the Twitch streamer being monitored. This is required to query the Twitch API for new clips.
- **Last Clip ID:** The ID of the most recently posted clip for a monitored streamer. This is used to prevent sending duplicate notifications.

The Bot **does not** collect or store any personally identifiable information beyond what is listed above. It does not store usernames, avatars, email addresses, or the content of your messages (other than processing the inputs for its slash commands).

### 2. How We Use Your Data

The collected data is used exclusively for the following purposes:

- To provide the core functionality of the Bot, which is to check for and post new Twitch clips.
- To manage the list of monitored streamers for each Discord server.
- To ensure the Bot sends notifications to the correct channel in the correct server.
- To send automated service-related direct messages to the user who set up a notification, in the event that the Bot can no longer function as configured (e.g., channel deleted, permissions lost).

### 3. Data Storage and Security

The collected data is stored in a JSON file on a secure server. We take reasonable measures to protect this data from unauthorized access, alteration, or destruction. However, no method of transmission over the internet or electronic storage is 100% secure, and we cannot guarantee its absolute security.

### 4. Data Retention

Data is retained only for as long as it is necessary to provide the service.

- When a server administrator removes a streamer using the `/removestreamer` command, all associated data (Twitch Streamer ID, Server ID, Channel ID, User ID, and Last Clip ID) for that entry is permanently deleted from our database.
- If the Bot is removed from a Discord server, a cleanup process will automatically run to delete all data associated with that Server ID.

### 5. Third-Party Services

The Bot relies on third-party services to function. By using the Bot, you are also subject to the privacy policies of these services:

- **Discord:** [Discord Privacy Policy](https://discord.com/privacy)
- **Twitch:** [Twitch Privacy Policy](https://www.twitch.tv/p/en/legal/privacy-notice/)

This Privacy Policy does not cover the data practices of these third-party services.

### 6. Your Rights and Data Deletion

You have control over the data you provide to the Bot.

- **Access and Viewing:** You can view all monitored streamers and their associated notification channels on your server by using the `/liststreamers` command.
- **Deletion:** A user with "Manage Channels" permissions can permanently delete a monitoring configuration and its associated data using the `/removestreamer` command. Removing the Bot from the server will also result in the deletion of all associated data.

If you have concerns about your data that cannot be resolved through the Bot's commands, please contact us directly.

### 7. Children's Privacy

The Bot does not knowingly collect any personally identifiable information from children under the age of 13, in compliance with the Children's Online Privacy Protection Act (COPPA) and Discord's own Terms of Service. If you believe we have inadvertently collected such information, please contact us immediately so we can take steps to remove it.

### 8. Changes to this Policy

We may update this Privacy Policy from time to time. We will notify you of any significant changes. Your continued use of the Bot after such changes constitutes your acceptance of the new Privacy Policy.

### 9. Contact

If you have any questions about this Privacy Policy, please contact us at `dinu@dinushay.de`.
