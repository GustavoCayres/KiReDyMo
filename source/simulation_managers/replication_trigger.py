from collections import defaultdict
from random import Random

from source.simulation_managers.replication import Replication


class ReplicationTrigger:
    def __init__(self, chromosome, strand, available_resources):
        self.chromosome = chromosome
        self.replication_origins = chromosome.replication_origins
        self.dna_strand = strand
        self.random_generator = Random()
        self.available_resources = available_resources * [True]

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

    def start_random_origin(self, replications, trigger_probability, step):
        if not self.update_start_probabilities():
            return

        for i, resource in enumerate(self.available_resources):
            if not resource or self.random_generator.random() >= trigger_probability:
                continue

            r = self.random_generator.random()
            for origin, probability in self.start_probabilities.items():
                r -= probability
                if r < 0:
                    self.available_resources[i] = False
                    self.trigger_origin(replications=replications, origin=origin, step=step)

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
