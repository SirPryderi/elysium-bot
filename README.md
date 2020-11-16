# Elysium Bot

Elysium Bot is a Discord bot that helps with Disco Elysium based campaigns. It is backed by a Google Sheet spreadsheet with the character information.

## Inviting the bot

To invite the bot to your channel, press [here](https://discord.com/api/oauth2/authorize?client_id=777603092321402932&permissions=1379392&scope=bot).

## Commands

### `!r`

Performs a dice roll in the current channel (or DM).

### `!r <skill name>`

Performs a dice roll + skill value for a current player. The player name must match the one specified in the spreadsheet. The bot must be authorized to access Google Docs before running this command.

### `!elysium-bot authorize`

Performs authorization with Google Account to allow access to spreadsheets.