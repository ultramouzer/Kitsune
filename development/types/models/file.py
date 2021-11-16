from .base import Database_Model


class File(Database_Model):
    name: str
    path: str
