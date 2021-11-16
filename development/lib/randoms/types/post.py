from datetime import datetime

from typing import Optional, TypedDict, List
from .comment import Random_Comment
from .file import Random_File


class Random_Post(TypedDict):
    id: str
    user: str
    published: datetime
    content: Optional[str]
    title: Optional[str]
    files: Optional[List[Random_File]]
    comments: Optional[List[Random_Comment]]
    edited: Optional[datetime]
