from typing import TypedDict


class Database_Model(TypedDict):
    """
    A model for saving into a database.
    """


class Query_Args(TypedDict):
    """
    Default query arguments for a model.
    Assumed to be transformed beforehand.
    """
    keys: str
    values: str
