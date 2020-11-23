import random
from discord.abc import Messageable
from discord.member import Member
from discord.ext import commands

from ..sheets.engine import SheetsEngine
from ..emojis import numbers


class Roll(commands.Cog):
  def __init__(self, sheet: SheetsEngine) -> None:
    self.sheet = sheet

  @commands.guild_only()
  @commands.command(aliases=["r"])
  async def roll(self, ctx: commands.Context, *skill):
    """Rolls two d6 dice. You can optionally pass a skill to do a skill check (e.g.: !r drama)."""
    if len(skill):
      await self._roll_skill(ctx.channel, ctx.author, " ".join(skill))
    else:
      await self._roll(ctx.channel, ctx.author)

  async def _roll(self, channel: Messageable, author: Member):
    user_id = author.id
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    await self.check_critical(d1, d2, channel)
    await channel.send(f"<@{user_id}> rolled:\n{numbers[d1]} {numbers[d2]} = **{total}**")

  async def _roll_skill(self, channel: Messageable, author: Member, skill_name: str):
    async with channel.typing():
      server = str(channel.guild.id)
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
