from lib.mafia.player import Player, Role

from random import shuffle


class Game:
    role_list = [
        Role.civilian,
        Role.civilian,
        Role.sheriff,
        Role.mafia
    ]

    def __init__(self, player_count):
        self.player_count = player_count

        self.players = []
        self.init_players()

    def init_players(self):
        trunc_role_list = self.role_list[:self.player_count]

        shuffle(trunc_role_list)

        for role in trunc_role_list:
            new_player = Player(role)
            self.players.append(new_player)
