from lib.users.user import User

from lib.simple_storage import SimpleStorage


class UserManager(SimpleStorage):
    def __init__(self):
        super().__init__()

    def add(self, username):
        new_user = User(username)
        return super().add(new_user)

    def get_user_session(self, user_id):
        return self[user_id].session_id

    def user_join_session(self, user_id, session_id):
        self[user_id].session_id = session_id
