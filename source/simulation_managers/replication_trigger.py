from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    random_number_generator = Random()
    random_number_generator.seed()

    @classmethod
    def set_seed(cls, seed):
        cls.random_number_generator.seed(seed)

    def __init__(self, replication_origins):
        self.replication_origins = replication_origins
        self.start_probabilities = {}
        for origin in self.replication_origins:
            self.start_probabilities[origin] = origin.score

    def start_random_origin(self):
        if not self.update_start_probabilities():
            return None, None

        r = self.random_float()
        for origin in self.replication_origins:
            r -= self.start_probabilities[origin]
            if r < 0:
                origin.score = 0
                return Replication(origin, -1), Replication(origin, 1)

        return None, None

    def update_start_probabilities(self):
        denominator = 0
        for origin in self.replication_origins:
            denominator += origin.score
        if denominator == 0:
            return False
        for origin, probability in self.start_probabilities.items():
            self.start_probabilities[origin] = origin.score/denominator
        return True

    def random_float(self):
        return self.random_number_generator.random()
