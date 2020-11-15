import discord
import random
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

dice = {
    1: "⚀",
    2: "⚁",
    3: "⚂",
    4: "⚃",
    5: "⚄",
    6: "⚅"
}

numbers = {
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
    6: ":six:"
}


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author.bot:
    return

  if message.content == '!r':
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    await message.channel.send(f"{numbers[d1]} {numbers[d2]} = **{total}**")

  if re.match('!r \w+', message.content):
    await message.channel.send(f"Not implemented!")


client.run(os.getenv("DISCORD_TOKEN"))
