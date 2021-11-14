from datetime import datetime

from typing import TypedDict, Optional, List
from .file import Random_File


class Random_DM(TypedDict):
    """
    `user` is an id of artist who sent the DM
    """
    id: str
    published: datetime
    user: str
    content: Optional[str]
    files: Optional[List[Random_File]]
