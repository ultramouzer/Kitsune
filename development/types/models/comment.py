from datetime import datetime
from typing import Optional

from .base import Database_Model


class Comment(Database_Model):
    id: str
    post_id: str
    commenter: str
    service: str
    content: str
    published: datetime
    parent_id: Optional[str]
