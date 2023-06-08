from __future__ import print_function

import sys
sys.path.append('.')

import logging

import grpc
from proto import mafia_pb2
from proto import mafia_pb2_grpc

from lib.argv_parser import parse_argv

from client.client_controller import ClientController
from client.cli import CLI
from client.player_gui import PlayerGUI


def run():
    args = parse_argv()
    args.bot = True

    channel = grpc.insecure_channel(args.server_address)

    stub = mafia_pb2_grpc.MafiaStub(channel)
    client_controller = ClientController(stub, args)

    gui = PlayerGUI()

    cli = CLI(client_controller, gui)

    gui.set_cli(cli)
    gui.flush_log()
    gui.mainloop()

    channel.close()


if __name__ == '__main__':
    logging.basicConfig()
    run()
