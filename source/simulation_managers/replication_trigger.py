from collections import defaultdict
from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    def __init__(self, chromosome, strand):
        self.chromosome = chromosome
        self.replication_origins = chromosome.replication_origins
        self.dna_strand = strand
        self.random_generator = Random()

        self.origin_trigger_log = defaultdict(list)
        self.number_of_origins = 0
        self.start_probabilities = {}

    def trigger_origin(self, replications, origin, step):
        origin.score = 0
        self.origin_trigger_log[step].append(origin.position)
        self.number_of_origins += 1
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
        self.update_start_probabilities()

    def start_random_origin(self, replications, trigger_probability, step, available_resources):
        if not self.update_start_probabilities():
            return

        for i in range(available_resources[0]):
            if self.random_generator.random() >= trigger_probability:
                continue

            r = self.random_generator.random()
            for origin, probability in self.start_probabilities.items():
                r -= probability
                if r < 0:
                    available_resources[0] -= 2
                    self.trigger_origin(replications=replications, origin=origin, step=step)
                    break

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
