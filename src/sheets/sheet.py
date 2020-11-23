from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


class Sheet:
  def __init__(self, sheet_id: str, waiting_token: bool = False) -> None:
    self.sheet_id: str = sheet_id
    self.waiting_token = waiting_token
    self.creds: Optional[Credentials] = None

  def keep_authenticated(self) -> None:
    if self.creds and self.creds.expired and self.creds.refresh_token:
      print("Attempting to re-authenticate client with refresh token")
      self.creds.refresh(Request())
      return True
    return False
