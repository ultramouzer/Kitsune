from datetime import datetime

from typing import TypedDict


class Service_Key_DB(TypedDict):
    """
    Minimal dict required for saving to database.
    """
    service: str
    key: str
    contributor_id: str
    discord_channel_ids: str


class Required(TypedDict):
    service: str
    encrypted_key: str
    contributor_id: int


class Service_Key(Required, total=False):
    id: str
    discord_channel_ids: str
    added: datetime
    dead: bool
