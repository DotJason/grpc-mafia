from __future__ import print_function
from enum import Enum

from lib.argv_parser import parse_argv

import logging
import time

import grpc
from proto import mafia_pb2
from proto import mafia_pb2_grpc

from lib.argv_parser import parse_argv


class CheckValidPlayerIdStatus(Enum):
    valid = 0,
    not_an_integer = 1,
    out_of_range = 2


class ClientController:
    def __init__(self, stub: mafia_pb2_grpc.MafiaStub, args):
        self.stub = stub

        self.username = args.username
        self.is_bot = args.bot

        self.user_id = None
        self.session_id = None
        self.player_id = None
        self.role = None
        self.game_status = None
        self.players = None
        self.day_count = 0
        self.action_cooldown = False
        self.last_checked_mafia_id = None
        self.last_revealed_player_id = None

    def connect(self):
        self.user_id = self.stub.Connect(mafia_pb2.UserName(name=self.username)).id

    def wait_for_session(self):
        while self.session_id is None:
            time.sleep(1)

            response = self.stub.GetSession(mafia_pb2.UserId(id=self.user_id))

            if response.is_session_present:
                self.session_id = response.session_id
                self.player_id = response.player_id
                self.role = response.role

    def wait_for_new_game_status(self):
        while True:
            time.sleep(1)

            response = self.stub.GetGameStatus(mafia_pb2.UserId(id=self.user_id))

            if response.status != self.game_status:
                self.game_status = response.status

                if self.game_status == mafia_pb2.DAY:
                    self.day_count += 1

                self.action_cooldown = False

                return

    def wait_for_new_reveal(self):
        while True:
            time.sleep(1)
            response = self.stub.GetLastRevealed(mafia_pb2.UserId(id=self.user_id))

            if not response.has_been_revealed:
                continue

            if response.player_id != self.last_revealed_player_id:
                self.last_revealed_player_id = response.player_id

                return

    def get_players(self):
        self.players = list(self.stub.GetPlayers(mafia_pb2.UserId(id=self.user_id)))

    def vote(self, player_id):
        return self.stub.Vote(mafia_pb2.TargetRequest(source_user_id=self.user_id, target_player_id=player_id))

    def vote_end_day(self):
        return self.stub.VoteEndDay(mafia_pb2.UserId(id=self.user_id))

    def mafia_action(self, player_id):
        self.action_cooldown = True

        return self.stub.MafiaAction(mafia_pb2.TargetRequest(source_user_id=self.user_id, target_player_id=player_id))

    def sheriff_action(self, player_id):
        self.action_cooldown = True
        if self.is_player_mafia(player_id):
            self.last_checked_mafia_id = player_id

        return self.stub.SheriffAction(mafia_pb2.TargetRequest(source_user_id=self.user_id, target_player_id=player_id))

    def reveal(self):
        player_id = self.last_checked_mafia_id

        return self.stub.SheriffReveal(mafia_pb2.TargetRequest(source_user_id=self.user_id, target_player_id=player_id))

    def check_valid_player_id(self, player_id):
        if not player_id.isdigit():
            return CheckValidPlayerIdStatus.not_an_integer

        player_id = int(player_id)

        if player_id >= len(self.players):
            return CheckValidPlayerIdStatus.out_of_range

        return CheckValidPlayerIdStatus.valid

    def is_alive(self, player_id):
        return self.players[player_id].status == mafia_pb2.ALIVE

    def is_ghost(self, player_id):
        return self.players[player_id].status == mafia_pb2.GHOST

    def is_self_ghost(self):
        return self.players[self.player_id].status == mafia_pb2.GHOST

    def is_player_self(self, player_id):
        return self.player_id == player_id

    def is_day(self):
        return self.game_status == mafia_pb2.DAY

    def is_first_day(self):
        return self.day_count == 1

    def is_mafia(self):
        return self.role == mafia_pb2.MAFIA

    def is_sheriff(self):
        return self.role == mafia_pb2.SHERIFF

    def is_player_mafia(self, player_id):
        return self.players[player_id].role == mafia_pb2.MAFIA

    def has_valid_last_checked(self):
        return self.last_checked_mafia_id is not None

    def is_game_started(self):
        return self.game_status is not None

    def is_game_ended(self):
        return self.game_status == mafia_pb2.MAFIA_WIN or self.game_status == mafia_pb2.CIVILIAN_WIN

    def is_role_revealed(self, player_id):
        return self.players[player_id].is_role_revealed

    def can_show_role(self, player_id):
        return self.is_player_self(player_id) or self.is_ghost(player_id) or self.is_role_revealed(player_id)
