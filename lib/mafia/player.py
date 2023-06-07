from enum import Enum


class Role(Enum):
    civilian = 1
    mafia = 2
    sheriff = 3


class Status(Enum):
    alive = 1
    ghost = 2


class Player:
    def __init__(self, role: Role):
        self.role = role
        self.status = Status.alive
