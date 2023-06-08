from enum import Enum
from lib.users import User

from proto import mafia_pb2


class Player:
    def __init__(self, user: User, player_id: int, role: mafia_pb2.Role):
        self.user = user
        self.player_id = player_id
        self.role = role
        self.status = mafia_pb2.ALIVE
        self.action_cooldown = False
        self.is_role_revealed = False
