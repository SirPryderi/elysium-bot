import json
import discord
import random
import os
import re
from sheets_client import SheetsEngine
from dotenv import load_dotenv

from emojis import numbers

load_dotenv()

credentials = json.loads(os.getenv("GOOGLE_API_CREDENTIALS"))
spreadsheetId = os.getenv("SPREADSHEET_ID")

client = discord.Client()
sheet = SheetsEngine(credentials, spreadsheetId)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  sheet.load_authentication()


@client.event
async def on_message(message):
  if message.author.bot:
    return

  if message.channel.type == discord.enums.ChannelType.private:
    if sheet.waiting_auth:
      try:
        sheet.save_authentication(message.content)
      except:
        await message.channel.send(f":no_entry: Authentication failed!")
      else:
        await message.channel.send(f":white_check_mark: Authentication complete!")

  if message.content == '!elysium-bot authenticate':
    url = sheet.request_authentication()
    await message.channel.send(f"Click the url below and follow the instructions on screen.\n\n{url}\n\nOnce completed paste the code here as a message.")

  if message.content == '!r':
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    await message.channel.send(f"{numbers[d1]} {numbers[d2]} = **{total}**")

  if re.match('!r \w+', message.content):
    await message.channel.send(f"Not implemented!")


client.run(os.getenv("DISCORD_TOKEN"))
