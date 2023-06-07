from __future__ import print_function

import logging
import time

import grpc
from proto import mafia_pb2
from proto import mafia_pb2_grpc

from lib.argv_parser import parse_argv


class ClientController:
    def __init__(self, stub: mafia_pb2_grpc.MafiaStub):
        self.stub = stub

        self.user_id = None
        self.session_id = None

    def connect(self):
        self.user_id = self.stub.Connect(mafia_pb2.UserName(name='John Doe')).id
        print(f"Connected as user id {self.user_id}")

    def wait_for_session(self):
        print("Waiting for session...")

        while self.session_id is None:
            time.sleep(1)
            response = self.stub.GetSession(mafia_pb2.UserId(id=self.user_id))

            if response.is_session_present:
                self.session_id = response.session_id

        print(f"Joined session id {self.session_id}")
