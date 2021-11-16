from datetime import datetime
from typing import Optional

from .base import Database_Model


class User(Database_Model):
    id: str
    name: str
    service: str
    indexed: Optional[datetime]
    updated: Optional[datetime]
