from lib.users.user import User

from lib.simple_storage import SimpleStorage


class UserManager(SimpleStorage):
    def __init__(self):
        super().__init__()

    def add(self, username):
        new_user = User(username)
        return super().add(new_user)

    def user_join_session(self, user_id, session_id, player):
        self[user_id].join_session(session_id, player)

    def get_player_id_by_user_id(self, user_id):
        return self[user_id].player_id
