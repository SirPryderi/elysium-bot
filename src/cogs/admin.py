from discord.ext import commands

from ..sheets.engine import SheetsEngine


class Admin(commands.Cog):
  def __init__(self, sheet: SheetsEngine) -> None:
    self.sheet = sheet

  @commands.guild_only()
  @commands.command(alias=["s"])
  async def status(self, ctx: commands.Context) -> None:
    """Returns useful data about the bot status"""
    server = str(ctx.guild.id)
    lines = []

    async with ctx.channel.typing():
      try:
        sheets = self.sheet.get_sheets(server)
        lines.append("Sheet connection: :ok:")
        lines.append(f"Campaigns: {' | '.join(sheets)}")
      except:
        sheet = self.sheet.sheet_store.get(server)
        lines.append("Sheet connection: :warning:")
        lines.append(f"Sheet set: {sheet != None}")
        if sheet and sheet.creds != None:
          lines.append(f"Auth expired: {self.sheet.creds.expired}")

    await ctx.channel.send("\n".join(lines))

  @commands.guild_only()
  @commands.command()
  async def authenticate(self, ctx: commands.Context, sheet_id: str):
    """Authenticates the bot to your google sheet"""
    url = self.sheet.request_authentication(str(ctx.channel.guild.id), sheet_id)
    await ctx.channel.send(f"Click the url below and follow the instructions on screen.\n\n{url}\n\nOnce completed write the `!token YOUR_CODE_HERE` as a message.")

  @commands.guild_only()
  @commands.command(hidden=True)
  async def token(self, ctx: commands.Context, token: str):
    self.sheet.save_authentication(str(ctx.channel.guild.id), token)
    try:
      pass
    except:
      await ctx.channel.send(f":no_entry: Authentication failed!")
    else:
      await ctx.channel.send(f":white_check_mark: Authentication complete!")
