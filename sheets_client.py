from __future__ import print_function
import pickle
import os.path
from typing import Mapping
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SheetsEngine:
  def __init__(self, credentials: Mapping, sheetId: str):
    self.authenticated = False
    self.waiting_auth = False
    self.credentials = credentials
    self.sheetId = sheetId

  def request_authentication(self) -> str:
    self.flow = InstalledAppFlow.from_client_config(self.credentials, SCOPES)
    self.flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    url, _ = self.flow.authorization_url()
    self.waiting_auth = True
    return url

  def save_authentication(self, code) -> None:
    self.flow.fetch_token(code=code)
    creds = self.flow.credentials
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)
    self.creds = creds
    self.waiting_auth = False
    self.authenticated = True

  def load_authentication(self) -> None:
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
        self.creds = pickle.load(token)
        self.authenticated = True
