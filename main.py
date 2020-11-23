from file_credential_store import FileCredentialStore
from redis_credential_store import RedisCredentialStore
import discord
import random
import os
import re
from sheets_client import SheetsEngine
from dotenv import load_dotenv

from emojis import numbers

channel_type = discord.enums.ChannelType

load_dotenv()

client = discord.Client()
credential_store = RedisCredentialStore() if os.getenv("REDIS_URL") else FileCredentialStore()
sheet = SheetsEngine(credential_store)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


async def check_critical(d1, d2, channel):
  if d1 == d2 == 1:
    await channel.send(f":skull: Critical failure!")

  if d1 == d2 == 6:
    await channel.send(f":trophy: Critical success!")


@client.event
async def on_message(message: discord.Message):
  if message.author.bot:
    return

  # only in DMs
  if message.channel.type == channel_type.private:
    pass

  # only in text channels
  if message.channel.type == channel_type.text:
    server = str(message.guild.id)
    campaign = message.channel.name

    if sheet.waiting_auth:
      try:
        sheet.save_authentication(server, message.content)
      except:
        await message.channel.send(f":no_entry: Authentication failed!")
      else:
        await message.channel.send(f":white_check_mark: Authentication complete!")

    if message.content == '!elysium-bot status':
      lines = []

      async with message.channel.typing():
        try:
          sheets = sheet.get_sheets(server)
          lines.append("Sheet connection: :ok:")
          lines.append(f"Campaigns: {' | '.join(sheets)}")
        except:
          lines.append("Sheet connection: :warning:")
          lines.append(f"Authenticated: {sheet.creds != None}")
          if sheet.creds != None:
            lines.append(f"Auth expired: {sheet.creds.expired}")

      await message.channel.send("\n".join(lines))

    if re.match('!r \w+', message.content):
      async with message.channel.typing():
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)

        skill_name = message.content[3:].lower()
        user_name = message.author.name
        user_id = message.author.id
        # TODO: handle authentication issue
        try:
          characters = sheet.get_characters(server, campaign)
        except:
          await message.channel.send(f"An error has occurred. Is `{campaign}` a valid campaign sheet?")
          return

      if user_name not in characters:
        await message.channel.send(f"<@{user_id}> does not have a character.")
        return

      character = characters[user_name]

      if skill_name not in character["skills"]:
        await message.channel.send(f"`{skill_name}` is not a valid skill.")
        return

      skill = character["skills"][skill_name]
      total = d1 + d2 + skill

      await check_critical(d1, d2, message.channel)
      await message.channel.send(f"<@{user_id}> rolled:\n{numbers[d1]} {numbers[d2]} + {skill} ({skill_name}) = **{total}**")

  # everywhere

  if message.content == '!elysium-bot authenticate':
    url = sheet.request_authentication()
    await message.channel.send(f"Click the url below and follow the instructions on screen.\n\n{url}\n\nOnce completed paste the code here as a message.")

  if message.content == '!r':
    user_id = message.author.id
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    await check_critical(d1, d2, message.channel)
    await message.channel.send(f"<@{user_id}> rolled:\n{numbers[d1]} {numbers[d2]} = **{total}**")


client.run(os.getenv("DISCORD_TOKEN"))
