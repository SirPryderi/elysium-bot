from __future__ import print_function
import json
import os.path
from typing import Mapping
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .redis_credential_store import RedisCredentialStore

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SheetsEngine:
  def __init__(self, credential_store: RedisCredentialStore):
    self.credentials = json.loads(os.getenv("GOOGLE_API_CREDENTIALS"))
    self.sheetId = os.getenv("SPREADSHEET_ID")
    self.authenticated = False
    self.waiting_auth = False
    self.creds = None
    self.credential_store = credential_store

  def request_authentication(self) -> str:
    self.flow = InstalledAppFlow.from_client_config(self.credentials, SCOPES)
    self.flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    url, _ = self.flow.authorization_url()
    self.waiting_auth = True
    return url

  def save_authentication(self, server: str, code: str) -> None:
    self.flow.fetch_token(code=code)
    creds = self.flow.credentials
    self.creds = creds
    self.credential_store.set(server, creds)
    self.waiting_auth = False
    self.authenticated = True

  def keep_authenticated(self, server: str) -> None:
    if self.creds and self.creds.expired and self.creds.refresh_token:
      print("Attempting to re-authenticate client with refresh token")
      self.creds.refresh(Request())
      self.credential_store.set(server, self.creds)

  def load_authentication(self, server: str) -> None:
    self.creds = self.credential_store.get(server)
    self.keep_authenticated(server)
    self.authenticated = True

  def get_service(self, server: str) -> None:
    self.load_authentication(server)
    return build('sheets', 'v4', credentials=self.creds)

  def get_sheets(self, server: str) -> list:
    result = self.get_service(server).spreadsheets().get(spreadsheetId=self.sheetId).execute()
    sheets = result.get('sheets', '')
    result = []
    for sheet in sheets:
      result.append(sheet["properties"]["title"])
    return result

  def get_characters(self, server: str, campaign: str) -> Mapping:
    service = self.get_service(server)
    # the range of the spreadsheet
    range = f'{campaign}!A1:U26'
    # call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range, majorDimension="COLUMNS").execute()
    values = result.get('values')

    # parse spreadsheet into a collection of character objects
    skills = {}
    characters = {}

    for i_column, column in enumerate(values):
      if column == []:
        continue

      if column[0] == "Character":
        for row_i, row in enumerate(column):
          if row in ["Skill", "Character", "Discord ID", ""]:
            continue
          skills[row.lower()] = row_i
      elif column[0] != "":
        name = column[0]
        player = column[1]
        character = {"name": name, "player": player, "skills": {}}
        for skill, skill_i in skills.items():
          character["skills"][skill] = int(values[i_column + 1][skill_i])
        characters[player] = character

    return characters
