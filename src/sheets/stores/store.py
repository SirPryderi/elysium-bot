class ISheetStore:
  from src.sheets.sheet import Sheet

  def get(self, server: str) -> Sheet:
    """Get sheet for a server id"""
    raise NotImplementedError

  def set(self, server: str, sheet: Sheet) -> None:
    """Sets the sheet for the server id"""
    raise NotImplementedError
