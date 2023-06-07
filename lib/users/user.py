class User:
    def __init__(self, name):
        self.name = name
        self.session_id = None

    def join_session(self, session_id):
        self.session_id = session_id
