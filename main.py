import os
from dotenv import load_dotenv

from src.elysium_bot import ElysiumBot
from src.sheets.stores.redis_store import RedisSheetStore
from src.sheets.stores.file_store import FileSheetsStore

load_dotenv()

credential_store = RedisSheetStore() if os.getenv("REDIS_URL") else FileSheetsStore()
elysium_bot = ElysiumBot(credential_store)

elysium_bot.run(os.getenv("DISCORD_TOKEN"))
