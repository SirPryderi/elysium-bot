from google.oauth2.credentials import Credentials


class ICredentialStore:
  def get(self, server: str) -> Credentials:
    """Get credentials for a server id"""
    raise NotImplementedError

  def set(self, server: str, creds: Credentials) -> None:
    """Sets the credentials for the server id"""
    raise NotImplementedError
