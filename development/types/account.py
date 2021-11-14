from datetime import datetime
from typing import Optional, TypedDict


class Account(TypedDict):
    id: int
    username: str
    password_hash: Optional[str]
    created_at: Optional[datetime]
