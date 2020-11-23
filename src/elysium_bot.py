from discord.ext import commands

from .sheets.engine import SheetsEngine
from .sheets.stores.store import ISheetStore
from .cogs.admin import Admin
from .cogs.roll import Roll


class ElysiumBot(commands.Bot):
  def __init__(self, sheet_store: ISheetStore):
    super().__init__(commands.when_mentioned_or("!"))
    self.credential_store = sheet_store
    self.sheet = SheetsEngine(sheet_store)
    self.add_cog(Admin(self.sheet))
    self.add_cog(Roll(self.sheet))

  async def on_ready(self):
    print('We have logged in as {0.user}'.format(self))
