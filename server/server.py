from concurrent import futures
from threading import Thread
# import logging

import grpc
import mafia_pb2
import mafia_pb2_grpc


from lib.users import User, UserManager


class MafiaServer(mafia_pb2_grpc.MafiaServicer):

    def __init__(self):
        self.user_manager = UserManager()

    def Connect(self, request: mafia_pb2.UserName, context: grpc.ServicerContext) -> mafia_pb2.UserId:
        new_user = User(request.name)
        user_id = self.user_manager.add_user(new_user)
        return mafia_pb2.UserId(id=user_id)

    def Disconnect(self, request: mafia_pb2.UserId, context: grpc.ServicerContext) -> mafia_pb2.DisconnectResponse:
        self.user_manager.remove_user(request.id)
        return mafia_pb2.DisconnectResponse()


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mafia_pb2_grpc.add_MafiaServicer_to_server(MafiaServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    # logging.basicConfig()
    serve()
