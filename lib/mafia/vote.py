class Vote:
    def __init__(self):
        self.votes = {}

    def cast(self, source, target):
        self.votes[source] = target

    def tally(self):
        if len(self.votes.keys()) == 0:
            return None

        return max(self.votes, key=self.votes.get)
