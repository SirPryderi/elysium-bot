import os
import redis
import pickle


class RedisCredentialStore:
  def __init__(self) -> None:
    self.redis = redis.from_url(os.getenv("REDIS_URL"))

  def get(self, server) -> str:
    return pickle.loads(self.redis.get(server))

  def set(self, server: str, creds) -> None:
    self.redis.set(server, pickle.dumps(creds))
