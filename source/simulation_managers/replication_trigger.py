from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    random_number_generator = Random()
    random_number_generator.seed()

    @classmethod
    def set_seed(cls, seed):
        cls.random_number_generator.seed(seed)

    def __init__(self, replication_origins, strand):
        self.dna_strand = strand
        self.replication_origins = replication_origins
        self.start_probabilities = {}

    def start_random_origin(self):
        if not self.update_start_probabilities():
            return None, None
        r = self.random_number_generator.random()
        for origin, probability in self.start_probabilities.items():
            r -= probability
            if r < 0:
                origin.score = 0
                return Replication(origin, -1, self.dna_strand), Replication(origin, 1, self.dna_strand)

    def update_start_probabilities(self):
        self.start_probabilities = {}
        denominator = 0
        for origin in self.replication_origins:
            denominator += origin.score
        if denominator == 0:
            return False
        for origin in self.replication_origins:
            self.start_probabilities[origin] = float(origin.score/denominator)

        return True
