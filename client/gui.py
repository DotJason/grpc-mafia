from abc import ABC, abstractmethod
import pika


class GUI:
    def __init__(self):
        self.cli = None

        self.chat_connection = None
        self.chat_channel = None
        self.queue_id = None

        self.chat_log_queue = []

    def init_chat_channel(self):
        self.queue_id = str(self.cli.client_context.session_id)

        self.chat_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            port=5672,
            connection_attempts=10,
            retry_delay=5
        ))

        self.chat_channel = self.chat_connection.channel()
        self.chat_channel.queue_declare(queue=self.queue_id)

    @abstractmethod
    def log(self, s):
        raise NotImplementedError

    @abstractmethod
    def log_buffer(self, s):
        raise NotImplementedError
