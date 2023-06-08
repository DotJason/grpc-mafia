class User:
    def __init__(self, name):
        self.name = name
        self.session_id = None
        self.player = None

    def join_session(self, session_id, player):
        self.session_id = session_id
        self.player = player
