from enum import StrEnum, auto


class State(StrEnum):
    NEW = auto()
    ACTIVE = auto()
    EXPIRED = auto()
