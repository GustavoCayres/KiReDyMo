from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    random_number_generator = Random()
    random_number_generator.seed()

    @classmethod
    def set_seed(cls, seed):
        cls.random_number_generator.seed(seed)

    def __init__(self, chromosome, strand):
        self.chromosome = chromosome
        self.replication_origins = chromosome.replication_origins
        self.dna_strand = strand

        self.start_probabilities = {}

    def start_random_origin(self, replications):
        if not self.update_start_probabilities():
            return None, None
        r = self.random_number_generator.random()
        for origin, probability in self.start_probabilities.items():
            r -= probability
            if r < 0:
                origin.score = 0
                if not self.dna_strand[origin.position]:
                    replications.append(Replication(origin=origin,
                                                    direction=-1,
                                                    speed=self.chromosome.replication_speed,
                                                    repair_duration=self.chromosome.replication_repair_duration,
                                                    strand=self.dna_strand))
                    replications.append(Replication(origin=origin,
                                                    direction=+1,
                                                    speed=self.chromosome.replication_speed,
                                                    repair_duration=self.chromosome.replication_repair_duration,
                                                    strand=self.dna_strand))

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
