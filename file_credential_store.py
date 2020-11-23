import os
import pickle
import redis
from os.path import join


class FileCredentialStore:
  def __init__(self) -> None:
    self.redis = redis.Redis(host='localhost', port=6379, db=0)

  def server_file_path(_, server: str) -> str:
    return join(".", "credentials", f"{server}.pickle")

  def get(self, server):
    path = self.server_file_path(server)
    if not os.path.exists(path):
      return
    with open(path, 'rb') as token:
      return pickle.load(token)

  def set(self, server: str, creds):
    path = self.server_file_path(server)
    with open(path, 'wb') as token:
      pickle.dump(creds, token)
