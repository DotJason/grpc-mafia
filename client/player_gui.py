from tkinter import Tk, Button, Text
from client.cli import CLI

from client.gui import GUI


class PlayerGUI(GUI, Tk):
    def __init__(self):
        super().__init__()

        self.cli = None

        self.title("GRPC Mafia GUI")

        self.log_text_field = Text(height=40, width=200, state='disabled')
        self.command_text_field = Text(height=1, width=200)

        self.command_text_field.bind("<Return>", self.handle_send_command)

        self.log_text_field.pack()
        self.command_text_field.pack()

        self.log_queue = []

    def set_cli(self, cli: CLI):
        self.cli = cli

    def add_log(self, s):
        self.log_text_field.configure(state='normal')
        self.log_text_field.insert('end', str(s))
        self.log_text_field.insert('end', '\n')
        self.log_text_field.configure(state='disabled')
        self.log_text_field.see("end")

    def log(self, s):
        self.add_log(s)

    def log_buffer(self, s):
        self.log_queue.append(str(s))

    def flush_log(self):
        for s in self.log_queue:
            self.add_log(s)
        self.log_queue = []
        self.after(1000, self.flush_log)

    def handle_send_command(self, event):
        text = self.command_text_field.get("1.0", 'end').strip()
        self.command_text_field.delete('1.0', 'end')

        self.add_log(f"> {text}")

        self.cli.process_command(text.split())
