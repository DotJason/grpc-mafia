from concurrent import futures
from threading import Thread
import logging

import grpc
from proto import mafia_pb2
from proto import mafia_pb2_grpc


from lib.users import UserManager
from lib.sessions import SessionManager


class MafiaServer(mafia_pb2_grpc.MafiaServicer):

    def __init__(self):
        self.user_manager = UserManager()
        self.session_manager = SessionManager(self.user_manager)

    def Connect(self, request: mafia_pb2.UserName, context: grpc.ServicerContext) -> mafia_pb2.UserId:
        user_id = self.user_manager.add(request.name)

        self.session_manager.add_user_to_queue(user_id)

        if self.session_manager.is_session_ready():
            self.session_manager.init_new_session()

        return mafia_pb2.UserId(id=user_id)

    def GetSession(self, request: mafia_pb2.UserId, context: grpc.ServicerContext) -> mafia_pb2.GetSessionResponse:
        session_id = self.user_manager.get_user_session(request.id)
        is_present = (session_id is not None)
        response = mafia_pb2.GetSessionResponse(session_id=session_id, is_session_present=is_present)

        return response

    def Disconnect(self, request: mafia_pb2.UserId, context: grpc.ServicerContext) -> mafia_pb2.DisconnectResponse:
        self.user_manager.remove(request.id)
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
    logging.basicConfig()
    serve()
