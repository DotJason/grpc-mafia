from lib.sessions.session import Session
from queue import Queue

from lib.simple_storage import SimpleStorage
from lib.users import UserManager


class NotEnoughPlayersException(BaseException):
    pass


class SessionManager(SimpleStorage):
    def __init__(self, user_manager_context: UserManager, player_count_for_session=4):
        super().__init__()

        self.user_manager_context = user_manager_context

        self.player_count_for_session = player_count_for_session

        self.user_queue = Queue()

    def add_user_to_queue(self, user_id):
        self.user_queue.put(user_id)

    def is_session_ready(self):
        return self.user_queue.qsize() >= self.player_count_for_session

    def init_new_session(self):
        if not self.is_session_ready():
            raise NotEnoughPlayersException

        player_list = []
        for i in range(self.player_count_for_session):
            player_list.append(self.user_queue.get())

        new_session = Session(player_list)
        session_id = self.add(new_session)

        for player in player_list:
            self.user_manager_context.user_join_session(player, session_id)

        print(f"Started session id {session_id}")

        return 0
