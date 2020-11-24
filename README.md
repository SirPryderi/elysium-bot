# Elysium Bot

Elysium Bot is a Discord bot that helps with Disco Elysium based campaigns.

It is backed by a Google Sheet spreadsheet ([template](https://docs.google.com/spreadsheets/d/1smSArAzT9QxktDFgokpl_SvkX7fLbuPbJpEsMZv9XAU/edit?usp=sharing)) with the characters information. Clone the template sheet (File -> Make a copy) and authorize the bot to access it to get started.

⚠ The channel where you make rolls must match the spreadsheet's tab name, e.g.: if you are planning to execute your commands in `#elysium-campaign` the spreadsheet tab name must be named `elysium-campaign`. You can have more than one simultaneous campaign by using multiple tabs.

## Inviting the bot

To invite the bot to your channel, press [**here**](https://discord.com/api/oauth2/authorize?client_id=777603092321402932&permissions=18496&scope=bot). After this you should authorize the bot to access your characters sheet, please see below how to do it.

## Commands

📝All commands can be executed mentioning the bot instead of using the `!` prefix.

### `!roll`

Performs a dice roll in the current channel (or DM).

### `!roll <skill name>`

Performs a dice roll + skill value for a current player. The player name must match the one specified in the spreadsheet. The bot must be authorized to access Google Docs before running this command.

### `!authorize <spreadsheet id>`

Performs authorization with Google Account to allow access to spreadsheets. The spreadsheet id can be found in the url, see https://developers.google.com/sheets/api/guides/concepts#spreadsheet_id.

### `!detach`

Opposite of `!authorize`, removes all information about your spreadsheet and attached authentication.

### `!status`

Returns status information about the bot. Useful to understand if something is wrong.

### `!help`

Displays all available commands.
