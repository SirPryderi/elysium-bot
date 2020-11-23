import discord
import random
from discord.abc import Messageable
from discord.member import Member

from .credential_stores.credential_store import ICredentialStore
from .sheets_client import SheetsEngine
from .emojis import numbers


class ElysiumBot:
  def __init__(self, client: discord.Client, credential_store: ICredentialStore):
    self.client = client
    self.credential_store = credential_store
    self.sheet = SheetsEngine(credential_store)

  ### AUTHENTICATION ###

  async def authenticate(self, channel: Messageable):
    url = self.sheet.request_authentication()
    await channel.send(f"Click the url below and follow the instructions on screen.\n\n{url}\n\nOnce completed paste the code here as a message.")

  async def save_authentication(self, channel: Messageable, token: str):
    try:
      self.sheet.save_authentication(str(channel.guild.id), token)
    except:
      await channel.send(f":no_entry: Authentication failed!")
    else:
      await channel.send(f":white_check_mark: Authentication complete!")

  ### UTILS ###

  def get_server(self, channel: Messageable) -> str:
    return str(channel.guild.id)

  async def status(self, channel: Messageable):
    lines = []

    async with channel.typing():
      try:
        sheets = self.sheet.get_sheets(self.get_server(channel))
        lines.append("Sheet connection: :ok:")
        lines.append(f"Campaigns: {' | '.join(sheets)}")
      except:
        lines.append("Sheet connection: :warning:")
        lines.append(f"Authenticated: {self.sheet.creds != None}")
        if self.sheet.creds != None:
          lines.append(f"Auth expired: {self.sheet.creds.expired}")

    await channel.send("\n".join(lines))

  ### ROLLS ###

  async def roll(self, channel: Messageable, author: Member):
    user_id = author.id
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    await self.check_critical(d1, d2, channel)
    await channel.send(f"<@{user_id}> rolled:\n{numbers[d1]} {numbers[d2]} = **{total}**")

  async def roll_skill(self, channel: Messageable, author: Member, skill_name: str):
    async with channel.typing():
      server = self.get_server(channel)
      campaign = channel.name

      d1 = random.randint(1, 6)
      d2 = random.randint(1, 6)

      user_name = author.name
      user_id = author.id
      # TODO: handle authentication issue
      try:
        characters = self.sheet.get_characters(server, campaign)
      except:
        await channel.send(f"An error has occurred. Is `{campaign}` a valid campaign sheet?")
        return

    if user_name not in characters:
      await channel.send(f"<@{user_id}> does not have a character.")
      return

    character = characters[user_name]

    if skill_name not in character["skills"]:
      await channel.send(f"`{skill_name}` is not a valid skill.")
      return

    skill = character["skills"][skill_name]
    total = d1 + d2 + skill

    await self.check_critical(d1, d2, channel)
    await channel.send(f"<@{user_id}> rolled:\n{numbers[d1]} {numbers[d2]} + {skill} ({skill_name}) = **{total}**")

  async def check_critical(self, d1, d2, channel):
    if d1 == d2 == 1:
      await channel.send(f":skull: Critical failure!")

    if d1 == d2 == 6:
      await channel.send(f":trophy: Critical success!")
