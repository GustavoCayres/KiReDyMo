import functools


@functools.total_ordering
class ReplicationOrigin:
    def __init__(self, position, score, chromosome):
        self.position = position
        self.score = score
        self.chromosome = chromosome
        self.replication_speed = chromosome.replication_speed
        self.replication_repair_duration = chromosome.replication_repair_duration

    def __str__(self):
        return str(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def __gt__(self, other):
        return self.position > other.position

    def __hash__(self):
        return hash(self.position)
