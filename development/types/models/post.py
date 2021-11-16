from datetime import datetime

from typing import TypedDict, List, Optional


class Post_Embed(TypedDict):
    pass


class Post_File(TypedDict):
    """
    `name` - original filename of the file.

    `path` - resulting path of the file.
    """
    name: str
    path: str


class Post(TypedDict):
    id: str
    user: str
    service: str
    file: Post_File
    attachments: List[Post_File]
    added: Optional[datetime]
    published: Optional[datetime]
    edited: Optional[datetime]
    embed: Optional[Post_Embed]
    shared_file: Optional[bool]
    title: Optional[str]
    content: Optional[str]
