from __future__ import print_function
from sys import argv

import logging

import grpc
import mafia_pb2
import mafia_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = mafia_pb2_grpc.MafiaStub(channel)
        user_id = stub.Connect(mafia_pb2.UserName(name='John Doe'))
        print(f"Connected as user id {user_id.id}")
        stub.Disconnect(user_id)


if __name__ == '__main__':
    logging.basicConfig()
    run()
