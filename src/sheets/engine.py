from __future__ import print_function
import json
import os.path
from src.sheets.sheet import Sheet
from typing import Mapping
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

from .stores.store import ISheetStore

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SheetsEngine:
  def __init__(self, sheet_store: ISheetStore):
    self.gca_credentials = json.loads(os.getenv("GOOGLE_API_CREDENTIALS"))
    self.sheet_store = sheet_store
    self.flows: Mapping[str, Flow] = {}

  def request_authentication(self, server: str, sheet_id: str) -> str:
    flow = Flow.from_client_config(self.gca_credentials, SCOPES)
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    url, _ = flow.authorization_url()
    sheet = Sheet(sheet_id=sheet_id, waiting_token=True)
    self.sheet_store.set(server, sheet)
    self.flows[server] = flow
    return url

  def save_authentication(self, server: str, code: str) -> None:
    print(f"Received token {code} for server {server}")
    sheet = self.sheet_store.get(server)
    self.flows[server].fetch_token(code=code)
    sheet.creds = self.flows[server].credentials
    sheet.waiting_token = False
    self.flows[server] = None

    self.sheet_store.set(server, sheet)

  def get_service(self, server: str):
    sheet = self.sheet_store.get(server)
    if not sheet:
      print("Sheet not found")
    if sheet.keep_authenticated():
      self.sheet_store.set(server, sheet)
    return build('sheets', 'v4', credentials=sheet.creds), sheet

  def get_sheets(self, server: str) -> list:
    service, sheet = self.get_service(server)
    result = service.spreadsheets().get(spreadsheetId=sheet.sheet_id).execute()
    sheets = result.get('sheets', '')
    result = []
    for sheet in sheets:
      result.append(sheet["properties"]["title"])
    return result

  def get_characters(self, server: str, campaign: str) -> Mapping:
    service, sheet = self.get_service(server)
    # the range of the spreadsheet
    range = f'{campaign}!A1:U26'
    # call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId=sheet.sheet_id, range=range, majorDimension="COLUMNS").execute()
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
