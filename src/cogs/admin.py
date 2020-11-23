from discord.ext import commands

from src.sheets_client import SheetsEngine


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
        lines.append("Sheet connection: :warning:")
        lines.append(f"Authenticated: {self.sheet.creds != None}")
        if self.sheet.creds != None:
          lines.append(f"Auth expired: {self.sheet.creds.expired}")

    await ctx.channel.send("\n".join(lines))

  @commands.guild_only()
  @commands.command()
  async def authenticate(self, ctx: commands.Context):
    """Authenticates the bot to your google sheet"""
    url = self.sheet.request_authentication()
    await ctx.channel.send(f"Click the url below and follow the instructions on screen.\n\n{url}\n\nOnce completed write the `!token YOUR_CODE_HERE` as a message.")

  @commands.guild_only()
  @commands.command(hidden=True)
  async def token(self, ctx: commands.Context, token: str):
    try:
      self.sheet.save_authentication(str(ctx.channel.guild.id), token)
    except:
      await ctx.channel.send(f":no_entry: Authentication failed!")
    else:
      await ctx.channel.send(f":white_check_mark: Authentication complete!")
