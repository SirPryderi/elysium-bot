import os
from dotenv import load_dotenv

from src.elysium_bot import ElysiumBot
from src.credential_stores.file_credential_store import FileCredentialStore
from src.credential_stores.redis_credential_store import RedisCredentialStore

load_dotenv()

credential_store = RedisCredentialStore() if os.getenv("REDIS_URL") else FileCredentialStore()
elysium_bot = ElysiumBot(credential_store)

elysium_bot.run(os.getenv("DISCORD_TOKEN"))
