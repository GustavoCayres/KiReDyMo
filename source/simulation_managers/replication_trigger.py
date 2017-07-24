from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    def __init__(self, chromosome, strand):
        self.chromosome = chromosome
        self.replication_origins = chromosome.replication_origins
        self.dna_strand = strand
        self.random_generator = Random()

        self.origin_trigger_log = {}
        self.start_probabilities = {}

    def trigger_origin(self, replications, origin, step):
        origin.score = 0
        self.origin_trigger_log[step] = origin.position
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

    def start_random_origin(self, replications, trigger_probability, step):
        if not self.update_start_probabilities():
            return

        for origin in self.chromosome.constitutive_origins:
            if self.start_probabilities[origin] > 0:
                return self.trigger_origin(replications=replications, origin=origin, step=step)

        if self.random_generator.random() >= trigger_probability:
            return

        r = self.random_generator.random()
        for origin, probability in self.start_probabilities.items():
            r -= probability
            if r < 0:
                return self.trigger_origin(replications=replications, origin=origin, step=step)

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
