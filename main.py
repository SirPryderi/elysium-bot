import discord
import os
import re
from dotenv import load_dotenv

from src.elysium_bot import ElysiumBot
from src.credential_stores.file_credential_store import FileCredentialStore
from src.credential_stores.redis_credential_store import RedisCredentialStore


channel_type = discord.enums.ChannelType

load_dotenv()

client = discord.Client()
credential_store = RedisCredentialStore() if os.getenv("REDIS_URL") else FileCredentialStore()
elysium_bot = ElysiumBot(client, credential_store)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.Message):
  channel = message.channel
  author = message.author

  if author.bot:
    return

  # only in DMs
  if channel.type == channel_type.private:
    pass

  # only in text channels
  if channel.type == channel_type.text:
    if elysium_bot.sheet.waiting_auth:
      await elysium_bot.save_authentication(channel, message.content)

    if message.content == '!elysium-bot status':
      await elysium_bot.status(channel)

    if re.match('!r \w+', message.content):
      await elysium_bot.roll_skill(channel, author, message.content[3:].lower())

  # everywhere
  if message.content == '!elysium-bot authenticate':
    await elysium_bot.authenticate(channel)

  if message.content == '!r':
    await elysium_bot.roll(channel, author)


client.run(os.getenv("DISCORD_TOKEN"))
