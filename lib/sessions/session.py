from lib.mafia.game import Game
from lib.mafia.vote import Vote


class Session:
    def __init__(self, users):
        self.users = users

        self.game = Game(self.users)
        self.vote = Vote()
        self.end_day_votes = set()
        self.last_revealed = None

    def cast_vote(self, source_player_id, target_player_id):
        self.vote.cast(source_player_id, target_player_id)

    def vote_end_day(self, player_id):
        self.end_day_votes.add(player_id)
        print("end_day_votes:", self.end_day_votes)

        if len(self.end_day_votes) == self.game.alive_players:
            self.execute()
            self.end_day()

    def mafia_action(self, source_player_id, target_player_id):
        print(f"Mafia kills player id {target_player_id}")
        self.game.player_action(source_player_id)
        self.game.kill(target_player_id)

    def sheriff_action(self, source_player_id, target_player_id):
        self.game.player_action(source_player_id)

    def reveal(self, player_id):
        self.last_revealed = player_id
        self.game.players[player_id].is_role_revealed = True

    def execute(self):
        player_id_to_execute = self.vote.tally()
        print(f"Voted to execute player id {player_id_to_execute}")

        self.vote = Vote()

        if player_id_to_execute is not None:
            self.game.kill(player_id_to_execute)

    def end_day(self):
        self.end_day_votes = set()
        self.game.start_night()
