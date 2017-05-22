import functools


@functools.total_ordering
class ReplicationOrigin:
    def __init__(self, position, score):
        self.position = position
        self.score = score

    def __str__(self):
        return str(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def __gt__(self, other):
        return self.position > other.position

    def __hash__(self):
        return hash(self.position)
