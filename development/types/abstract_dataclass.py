from dataclasses import dataclass
from abc import ABC

@dataclass
class Abstract_Dataclass(ABC):
    """
    Prevents abstract dataclasses from being instantiated.
    Source:
    https://stackoverflow.com/questions/60590442/abstract-dataclass-without-abstract-methods-in-python-prohibit-instantiation
    """
    def __new__(cls, *args, **kwargs):
        if cls == Abstract_Dataclass or cls.__bases__[0] == Abstract_Dataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)
