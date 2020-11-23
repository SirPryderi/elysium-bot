import os
import pickle
from os.path import join
from google.oauth2.credentials import Credentials


class FileCredentialStore:
  def server_file_path(_, server: str) -> str:
    return join(".", "credentials", f"{server}.pickle")

  def get(self, server: str) -> Credentials:
    path = self.server_file_path(server)
    if not os.path.exists(path):
      return None
    with open(path, 'rb') as token:
      return pickle.load(token)

  def set(self, server: str, creds: Credentials) -> None:
    path = self.server_file_path(server)
    with open(path, 'wb') as token:
      pickle.dump(creds, token)
