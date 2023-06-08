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

    def Connect(self, request, context):
        user_id = self.user_manager.add(request.name)

        self.session_manager.add_user_to_queue(user_id)

        if self.session_manager.is_session_ready():
            self.session_manager.init_new_session()

        return mafia_pb2.UserId(id=user_id)

    def GetSession(self, request, context):
        user = self.user_manager[request.id]
        session_id = user.session_id
        player_id = None
        role = None

        is_present = (session_id is not None)
        if is_present:
            player_id = user.player.player_id
            role = user.player.role

        response = mafia_pb2.GetSessionResponse(
            session_id=session_id,
            is_session_present=is_present,
            player_id=player_id,
            role=role
        )

        return response

    def GetPlayers(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.id)
        users = session.users

        for user_id in users:
            user = self.user_manager[user_id]

            response = mafia_pb2.Player(
                username=user.name,
                role=user.player.role,
                status=user.player.status,
                is_role_revealed=user.player.is_role_revealed
            )

            yield response

    def GetGameStatus(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.id)

        response = mafia_pb2.GetGameStatusResponse(
            status=session.game.status
        )

        return response

    def GetLastRevealed(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.id)
        player_id = session.last_revealed
        has_been_revealed = (player_id is not None)

        response = mafia_pb2.GetLastRevealedResponse(
            player_id=player_id,
            has_been_revealed=has_been_revealed
        )

        return response

    def Vote(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.source_user_id)
        source_player_id = self.user_manager[request.source_user_id].player.player_id
        session.cast_vote(source_player_id, request.target_player_id)

        return mafia_pb2.VoteResponse()

    def VoteEndDay(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.id)
        session.vote_end_day(self.user_manager[request.id].player.player_id)

        return mafia_pb2.VoteEndDayResponse()

    def MafiaAction(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.source_user_id)
        source_player_id = self.user_manager[request.source_user_id].player.player_id
        session.mafia_action(source_player_id, request.target_player_id)

        return mafia_pb2.MafiaActionResponse()

    def SheriffAction(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.source_user_id)
        source_player_id = self.user_manager[request.source_user_id].player.player_id
        session.sheriff_action(source_player_id, request.target_player_id)

        return mafia_pb2.SheriffActionResponse()

    def SheriffReveal(self, request, context):
        session = self.session_manager.get_session_by_user_id(request.source_user_id)
        session.reveal(request.target_player_id)

        return mafia_pb2.SheriffRevealResponse()

    def Disconnect(self, request, context):
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
