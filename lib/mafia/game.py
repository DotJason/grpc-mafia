from lib.mafia.player import Player
from proto import mafia_pb2

from random import shuffle


class Game:
    role_list = [
        mafia_pb2.CIVILIAN,
        mafia_pb2.CIVILIAN,
        mafia_pb2.MAFIA,
        mafia_pb2.SHERIFF
    ]

    def __init__(self, users):
        self.player_count = len(users)
        self.alive_players = self.player_count

        self.users = users
        self.players = []
        self.roles = []
        self.init_players()

        self.status = mafia_pb2.DAY

    def init_players(self):
        self.roles = self.role_list[:self.player_count]

        # shuffle(self.roles)

        for i, role in enumerate(self.roles):
            new_player = Player(self.users[i], i, role)
            self.players.append(new_player)

    def player_action(self, source_player_id):
        self.players[source_player_id].action_cooldown = True
        if self.can_start_day():
            self.start_day()

    def kill(self, player_id):
        print(f"Killed player id {player_id}")
        self.players[player_id].status = mafia_pb2.GHOST
        self.alive_players -= 1

    def start_night(self):
        print("Starting night")
        self.status = mafia_pb2.NIGHT
        self.check_win()

    def start_day(self):
        print("Starting day")
        self.status = mafia_pb2.DAY
        self.check_win()

    def can_start_day(self):
        for player in self.players:
            if player.role != mafia_pb2.CIVILIAN and not player.action_cooldown:
                return False

        return True

    def count_alive(self, role):
        res = 0
        for player in self.players:
            if player.role == role and player.status == mafia_pb2.ALIVE:
                res += 1

        return res

    def check_win(self):
        alive_mafias = self.count_alive(mafia_pb2.MAFIA)

        if alive_mafias == 0:
            self.status = mafia_pb2.CIVILIAN_WIN
            print("Game ended! Civilians win!")

        if alive_mafias * 2 == self.alive_players:
            self.status = mafia_pb2.MAFIA_WIN
            print("Game ended! Mafia wins!")
