from enum import StrEnum


class State(StrEnum):
    NEW = "new"
    ACTIVE = "active"
    EXPIRED = "expired"
