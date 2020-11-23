import os
import redis
import pickle
from google.oauth2.credentials import Credentials


class RedisCredentialStore:
  def __init__(self) -> None:
    self.redis = redis.from_url(os.getenv("REDIS_URL"))

  def get(self, server: str) -> Credentials:
    return pickle.loads(self.redis.get(server))

  def set(self, server: str, creds: Credentials) -> None:
    self.redis.set(server, pickle.dumps(creds))
