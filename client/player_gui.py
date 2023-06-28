import os
import pika
from threading import Thread
from tkinter import Tk, Button, Text
from client.cli import CLI

from client.gui import GUI


if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')


def add_message(s, text_field):
    if isinstance(s, bytes):
        s = str(s, "utf-8")

    text_field.configure(state='normal')
    text_field.insert('end', s)
    text_field.insert('end', '\n')
    text_field.configure(state='disabled')
    text_field.see("end")


class PlayerGUI(GUI, Tk):
    def __init__(self):
        Tk.__init__(self)
        GUI.__init__(self)

        self.title("GRPC Mafia GUI")

        section_width = 120

        self.log_text_field = Text(height=40, width=section_width, state='disabled')
        self.command_text_field = Text(height=1, width=section_width)
        self.chat_log_text_field = Text(height=40, width=section_width, state='disabled')
        self.chat_text_field = Text(height=1, width=section_width)

        self.command_text_field.bind("<Return>", self.handle_send_command)
        self.chat_text_field.bind("<Return>", self.handle_send_chat_message)

        self.log_text_field.grid(row=1, column=1)
        self.command_text_field.grid(row=2, column=1)
        self.chat_log_text_field.grid(row=1, column=2)
        self.chat_text_field.grid(row=2, column=2)

        self.log_queue = []

    def set_cli(self, cli: CLI):
        self.cli = cli

        def start_consume():
            chat_consume_connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost',
                port=5672,
                connection_attempts=10,
                retry_delay=5
            ))

            channel = chat_consume_connection.channel()
            channel.queue_declare(queue=self.queue_id)

            def callback(ch, method, properties, body):
                self.chat_log_queue.append(body)

            channel.basic_consume(
                queue=self.queue_id,
                on_message_callback=callback
            )

            channel.start_consuming()
            chat_consume_connection.close()

        chat_watcher = Thread(target=start_consume)
        chat_watcher.start()

        self.init_chat_channel()

        add_message("Welcome to the Mafia chat!", self.chat_log_text_field)

    def close_chat_connection(self):
        self.chat_connection.close()

    def log(self, s):
        add_message(s, self.log_text_field)

    def log_buffer(self, s):
        self.log_queue.append(str(s))

    def flush_logs(self):
        for s in self.log_queue:
            self.log(s)
        self.log_queue = []

        for s in self.chat_log_queue:
            add_message(s, self.chat_log_text_field)
        self.chat_log_queue = []

        self.after(500, self.flush_logs)

    def handle_send_command(self, event):
        text = self.command_text_field.get("1.0", 'end').strip()
        self.command_text_field.delete('1.0', 'end')

        self.log(f"> {text}")

        self.cli.process_command(text.split())

    def handle_send_chat_message(self, event):
        text = self.chat_text_field.get("1.0", 'end').strip()
        self.chat_text_field.delete('1.0', 'end')

        msg = f"{self.cli.client_context.username}: {text}"

        self.chat_channel.basic_publish(exchange='', routing_key=self.queue_id, body=msg)
