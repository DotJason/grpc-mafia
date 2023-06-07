from __future__ import print_function

import os
from threading import Thread

import logging

import grpc
from proto import mafia_pb2
from proto import mafia_pb2_grpc

from lib.argv_parser import parse_argv

from client.client_controller import ClientController


def run():
    args = parse_argv()
    print(args.username)

    with grpc.insecure_channel(args.server_address) as channel:
        stub = mafia_pb2_grpc.MafiaStub(channel)
        client_controller = ClientController(stub)
        client_controller.connect()

        client_controller.wait_for_session()

        # wait_for_session_thread = Thread(target=client_controller.wait_for_session)
        # wait_for_session_thread.start()


if __name__ == '__main__':
    logging.basicConfig()
    run()
