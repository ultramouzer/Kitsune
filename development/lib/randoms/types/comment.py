from datetime import datetime

from typing import Optional, TypedDict


class Random_Comment(TypedDict):
    """"""
    id: str
    commenter_id: str
    content: str
    published: datetime
    parent_id: Optional[str]
