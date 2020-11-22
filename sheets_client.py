from __future__ import print_function
import pickle
import os.path
from typing import Mapping
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
PICKLE = "token.pickle"

class SheetsEngine:
  def __init__(self, credentials: Mapping, sheetId: str):
    self.authenticated = False
    self.waiting_auth = False
    self.credentials = credentials
    self.creds = None
    self.sheetId = sheetId

  def pickle(self) -> None:
    with open(PICKLE, 'wb') as token:
      pickle.dump(self.creds, token)

  def unpickle(self) -> None:
    if not os.path.exists(PICKLE):
      return
    with open(PICKLE, 'rb') as token:
      self.creds = pickle.load(token)

  def request_authentication(self) -> str:
    self.flow = InstalledAppFlow.from_client_config(self.credentials, SCOPES)
    self.flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    url, _ = self.flow.authorization_url()
    self.waiting_auth = True
    return url

  def save_authentication(self, code: str) -> None:
    self.flow.fetch_token(code=code)
    creds = self.flow.credentials
    self.creds = creds
    self.pickle()
    self.waiting_auth = False
    self.authenticated = True

  def keep_authenticated(self) -> None:
    if self.creds and self.creds.expired and self.creds.refresh_token:
      print("Attempting to re-authenticate client with refresh token")
      self.creds.refresh(Request())
      self.pickle()

  def load_authentication(self) -> None:
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    self.unpickle()
    self.keep_authenticated()
    self.authenticated = True

  def get_service(self) -> None:
    self.keep_authenticated()
    self.service = build('sheets', 'v4', credentials=self.creds)

  def get_sheets(self) -> list:
    self.get_service()
    result = self.service.spreadsheets().get(spreadsheetId=self.sheetId).execute()
    sheets = result.get('sheets', '')
    result = []
    for sheet in sheets:
      result.append(sheet["properties"]["title"])
    return result

  def get_characters(self, campaign: str) -> Mapping:
    self.get_service()
    # the range of the spreadsheet
    range = f'{campaign}!A1:U26'
    # call the Sheets API
    sheet = self.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=self.sheetId, range=range, majorDimension="COLUMNS").execute()
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
