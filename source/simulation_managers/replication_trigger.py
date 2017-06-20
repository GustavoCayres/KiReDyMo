from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    def __init__(self, chromosome, strand):
        self.chromosome = chromosome
        self.replication_origins = chromosome.replication_origins
        self.dna_strand = strand
        self.random_generator = Random()

        self.triggered_origins = 0
        self.start_probabilities = {}

    def trigger_origin(self, replications, origin):
        origin.score = 0
        self.triggered_origins += 1
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

    def start_random_origin(self, replications, trigger_probability):
        if not self.update_start_probabilities():
            return

        if self.random_generator.random() >= trigger_probability:
            return

        r = self.random_generator.random()
        for origin, probability in self.start_probabilities.items():
            r -= probability
            if r < 0:
                self.trigger_origin(replications=replications, origin=origin)
                return

    def update_start_probabilities(self):
        self.start_probabilities = {}
        denominator = 0
        for origin in self.replication_origins:
            if self.dna_strand.is_position_duplicated(origin.position):
                origin.score = 0
            else:
                denominator += origin.score

        if denominator == 0:
            return False
        for origin in self.replication_origins:
            self.start_probabilities[origin] = float(origin.score/denominator)

        return True
