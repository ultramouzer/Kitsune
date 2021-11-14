from typing import List, TypedDict

from .dm import Random_DM
from .user import Random_User


class Random_Dataset(TypedDict):
    users: List[Random_User]
    dms: List[Random_DM]
