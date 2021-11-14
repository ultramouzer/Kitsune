from typing import TypedDict, List, Optional

from .post import Random_Post


class Random_User(TypedDict):
    id: str
    name: str
    posts: Optional[List[Random_Post]]
