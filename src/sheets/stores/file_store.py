import os
import pickle
from os.path import join

from src.sheets.sheet import Sheet


class FileSheetsStore:
  def server_file_path(_, server: str) -> str:
    return join(".", "sheets", f"{server}.pickle")

  def get(self, server: str) -> Sheet:
    path = self.server_file_path(server)
    if not os.path.exists(path):
      return None
    with open(path, 'rb') as token:
      return pickle.load(token)

  def set(self, server: str, sheet: Sheet) -> None:
    path = self.server_file_path(server)
    with open(path, 'wb') as token:
      pickle.dump(sheet, token)
