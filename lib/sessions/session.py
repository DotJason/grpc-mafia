from lib.mafia.game import Game


class Session:
    def __init__(self, users):
        self.users = users
        self.user_count = len(users)

        self.game = Game(self.user_count)
