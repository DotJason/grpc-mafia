from client.cli import CLI
import time
from random import choice, randint
from lib.name_generator import random_name

from client.gui import GUI


class BotGUI(GUI):
    def __init__(self):
        super().__init__()

    def set_cli(self, cli: CLI):
        self.cli = cli

        self.init_chat_channel()

    def mainloop(self):
        client_context = self.cli.client_context

        while True:
            time.sleep(1)
            self.cli.process_command(self.generate_bot_command())

            if randint(0, 2) == 0:
                msg = f"{client_context.username}: {random_name(capitalize_first_letter=False)}"
                self.chat_channel.basic_publish(exchange='', routing_key=self.queue_id, body=msg)

    def log(self, s):
        print(s)

    def log_buffer(self, s):
        print(s)

    def generate_bot_command(self):
        client_context = self.cli.client_context

        alive_player_ids = []
        for i in range(len(client_context.players)):
            if client_context.is_alive(i) and i != client_context.player_id:
                alive_player_ids.append(str(i))

        res = [['wait']]
        if client_context.is_self_ghost():
            return choice(res)

        if client_context.is_day():
            res.append([
                'vote',
                choice(alive_player_ids)
            ])

            res.append([
                'end_day'
            ])

            if client_context.is_sheriff():
                res.append([
                    'reveal'
                ])
        else:
            if client_context.is_mafia():
                res.append([
                    'kill',
                    choice(alive_player_ids)
                ])
            elif client_context.is_sheriff():
                res.append([
                    'check',
                    choice(alive_player_ids)
                ])

        return choice(res)
