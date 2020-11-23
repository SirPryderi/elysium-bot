from discord.ext import commands

from .credential_stores.credential_store import ICredentialStore
from .sheets_client import SheetsEngine
from .cogs.admin import Admin
from .cogs.roll import Roll


class ElysiumBot(commands.Bot):
  def __init__(self, credential_store: ICredentialStore):
    super().__init__(commands.when_mentioned_or("!"))
    self.credential_store = credential_store
    self.sheet = SheetsEngine(credential_store)
    self.add_cog(Admin(self.sheet))
    self.add_cog(Roll(self.sheet))

  async def on_ready(self):
    print('We have logged in as {0.user}'.format(self))
