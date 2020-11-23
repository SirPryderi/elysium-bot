import os
import redis
import pickle

from src.sheets.sheet import Sheet


class RedisSheetStore:
  def __init__(self) -> None:
    self.redis = redis.from_url(os.getenv("REDIS_URL"))

  def get(self, server: str) -> Sheet:
    return pickle.loads(self.redis.get(server))

  def set(self, server: str, sheet: Sheet) -> None:
    self.redis.set(server, pickle.dumps(sheet))
