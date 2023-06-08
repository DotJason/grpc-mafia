import time
from threading import Thread
from prettytable import PrettyTable

from proto import mafia_pb2

from client.client_controller import ClientController, CheckValidPlayerIdStatus


def help_line(parts):
    (left, right) = parts

    if right is None:
        return left

    return f"{left}\t-\t{right}"


def help_string():
    lines = [
        ('General commands:', None),
        ('help', 'This command'),
        ('players', 'List player ids, names, known roles and statuses'),
        ('', None),
        ('Game commands:', None),
        ('vote PLAYER_ID', 'Vote to execute the player with id PLAYER_ID during the (non-first) day'),
        ('end_day', 'Vote to end the day. The day concludes when all players have sent this command'),
        ('', None),
        ('Role-specific commands:', None),
        ('Mafia:', None),
        ('kill PLAYER_ID', 'Kill the player with id PLAYER_ID during the night'),
        ('Sheriff:', None),
        ('check PLAYER_ID', 'Check whether the player with id PLAYER_ID is mafia or not'),
        ('reveal', 'If sheriff has checked a mafia, this will reveal the result of the last such check to all players')
    ]

    return '\n'.join(map(help_line, lines))


role_labels = {
    0: '?',
    1: 'Civilian',
    2: 'Mafia',
    3: 'Sheriff'
}

status_labels = {
    0: 'Alive',
    1: 'Ghost'
}


class CLI:
    def __init__(self, client_context: ClientController, gui):
        self.client_context = client_context
        self.gui = gui

        self.client_context.connect()
        print(f"Connected username {self.client_context.username} as user id {self.client_context.user_id}")

        print("Waiting for session...")
        self.client_context.wait_for_session()
        print(f"Joined session id {self.client_context.session_id} as role: {role_labels[self.client_context.role]}")

        self.log("Welcome to the Mafia game GUI! Type 'help' for the list of available commands")

        self.client_context.get_players()

        game_status_watcher = Thread(target=self.watch_game_status)
        game_status_watcher.start()

        reveals_watcher = Thread(target=self.watch_reveals)
        reveals_watcher.start()

    def log(self, s, buffer=False):
        self.gui.log(s)

    def print_help(self, *args):
        self.log(help_string())

    def wait(self):
        pass

    def process_command(self, s):
        cmd_map = {
            'help': self.print_help,
            'players': self.players,
            'vote': self.vote,
            'end_day': self.end_day,
            'kill': self.kill,
            'check': self.check,
            'reveal': self.reveal,
            'wait': self.wait
        }

        non_game_commands = ['help', 'players', 'wait']

        if len(s) == 0:
            s.append('')

        print("I want to do this:", ' '.join(s))

        command = s[0]

        if command not in non_game_commands:
            if not self.client_context.is_game_started():
                self.log("The game has not started yet! Please wait a bit")
                return

            if self.client_context.is_game_ended():
                self.log("The game has ended! Please restart the client app")
                return

            if self.client_context.is_ghost(self.client_context.player_id):
                self.log("You are a ghost! You can't do actions anymore, though you can watch the rest of the game")
                return

        if command not in cmd_map:
            self.log(f"Unknown command '{command}'! Type 'help' for the list of available commands")
            return

        cmd_map[command](*s[1:])

    def watch_game_status(self):
        while not self.client_context.is_game_ended():
            self.client_context.wait_for_new_game_status()

            self.client_context.get_players()

            day_num = self.client_context.day_count

            log_mess = ""

            if self.client_context.game_status == mafia_pb2.DAY:
                log_mess = f"Day {day_num} begins!"
            elif self.client_context.game_status == mafia_pb2.NIGHT:
                log_mess = f"Night {day_num} begins!"
            elif self.client_context.game_status == mafia_pb2.MAFIA_WIN:
                log_mess = "Mafia wins!"
            else:
                log_mess = "Civilians win!"

            self.log(log_mess, buffer=True)

            self.log("Current player status:", buffer=True)
            self.players(buffer=True)

    def watch_reveals(self):
        while not self.client_context.is_game_ended():
            self.client_context.wait_for_new_reveal()

            revealed_id = self.client_context.last_revealed_player_id
            self.log(f"The Sheriff has revealed a Mafia! It was the player with id {revealed_id}", buffer=True)

            self.players(buffer=True)

    def players(self, *args, buffer=False):
        self.client_context.get_players()

        t = PrettyTable(["id", "username", "role", "status"])

        for i, player in enumerate(self.client_context.players):
            displayed_role = 0
            if self.client_context.is_game_ended() or self.client_context.can_show_role(i):
                displayed_role = player.role
            t.add_row([i, player.username, role_labels[displayed_role], status_labels[player.status]])

        self.log(t, buffer=buffer)

    def vote(self, *args):
        if len(args) == 0:
            self.log("No player id specified!")
            return

        player_id = args[0]
        if not self.check_valid_player_id(player_id):
            return

        player_id = int(player_id)

        if not self.client_context.is_day():
            self.log("Can't vote during the night!")
            return

        if self.client_context.is_first_day():
            self.log("Can't vote during the first day!")
            return

        if self.client_context.is_player_self(player_id):
            self.log("Can't vote for yourself!")
            return

        if self.client_context.is_ghost(player_id):
            self.log("Can't vote for ghosts!")
            return

        self.client_context.vote(player_id)
        self.log(f"Successfully voted to execute player with id {player_id}.")

    def end_day(self, *args):
        if not self.client_context.is_day():
            self.log("Can't vote to end day during the night!")
            return

        self.client_context.vote_end_day()
        self.log("Successfully voted to end the day.")

    def kill(self, *args):
        if len(args) == 0:
            self.log("No player id specified!")
            return

        player_id = args[0]
        if not self.check_valid_player_id(player_id):
            return

        player_id = int(player_id)

        if not self.client_context.is_mafia():
            self.log("Only Mafia can kill!")
            return

        if self.client_context.is_day():
            self.log("Can't kill during the day!")
            return

        if self.client_context.is_player_self(player_id):
            self.log("Can't kill yourself!")
            return

        if self.client_context.is_ghost(player_id):
            self.log("Can't kill ghosts!")
            return

        if self.client_context.action_cooldown:
            self.log("Already killed this night!")
            return

        self.client_context.mafia_action(player_id)
        self.log(f"Successfully killed player with id {player_id}.")

    def check(self, *args):
        if len(args) == 0:
            self.log("No player id specified!")
            return

        player_id = args[0]
        if not self.check_valid_player_id(player_id):
            return

        player_id = int(player_id)

        if not self.client_context.is_sheriff():
            self.log("Only Sheriff can check!")
            return

        if self.client_context.is_day():
            self.log("Can't check during the day!")
            return

        if self.client_context.is_player_self(player_id):
            self.log("Can't check yourself!")
            return

        if self.client_context.is_ghost(player_id):
            self.log("Can't check ghosts!")
            return

        if self.client_context.action_cooldown:
            self.log("Already checked this night!")
            return

        self.client_context.sheriff_action(player_id)
        res = "Mafia" if self.client_context.is_player_mafia(player_id) else "Not Mafia"
        self.log(f"Successfully checked player with id {player_id}. Result: {res}")

    def reveal(self, *args):
        if not self.client_context.has_valid_last_checked():
            self.log("You have not checked any Mafia yet!")
            return

        self.client_context.reveal()

    def check_valid_player_id(self, player_id):
        status = self.client_context.check_valid_player_id(player_id)

        if status != CheckValidPlayerIdStatus.valid:
            if status == CheckValidPlayerIdStatus.not_an_integer:
                self.log("Player id must be an integer!")
            elif status == CheckValidPlayerIdStatus.out_of_range:
                self.log(f"Player id must be less than the number of players ({len(self.client_context.players)})")

            return False

        return True
