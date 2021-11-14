from datetime import datetime
from typing import Optional, TypedDict

from .base import Database_Model


class DM_File(TypedDict):
    """"""


class DM_Embed(TypedDict):
    """"""


class DM(Database_Model):
    id: str
    import_id: str
    contributor_id: str
    published: datetime
    user: str
    service: str
    file: DM_File
    added: Optional[datetime]
    content: Optional[str]
    embed: Optional[DM_Embed]
