import itertools
from collections import defaultdict


class EncounterVerifier:
    """ Controls the encounters between two replication machineries. """

    def __init__(self, chromosome):
        self.chromosome_length = chromosome.length
        self.number_of_origins = len(chromosome.replication_origins)
        self.chromosome_start_done = False
        self.chromosome_end_done = False
        self.where_encounter_occurred = None

    def will_end(self, replication):
        return self.where_encounter_occurred[replication] is not None

    def resulting_position_after_encounter(self, replication):
        return self.where_encounter_occurred[replication]

    def verify_encounter_between(self, replication_1, replication_2):
        """ Verifies whether there is an imminent encounter between the replications' machineries. """

        if replication_1.finished or replication_2.finished or replication_1.direction == replication_2.direction:
            return

        if 0 < -replication_1.direction * replication_1.fork_position +\
                -replication_2.direction * replication_2.fork_position <= replication_1.speed + replication_2.speed:
            replication_1.finish()
            replication_2.finish()

    def verify_encounters(self, replications):
        self.where_encounter_occurred = defaultdict(lambda: None)

        for pair in itertools.combinations(replications, 2):
            self.verify_encounter_between(*pair)

        for replication in replications:
            if replication.is_active():
                if replication.fork_position + replication.direction * replication.speed < 0:
                    replication.finish()
                elif replication.fork_position + replication.direction * replication.speed >= self.chromosome_length:
                    replication.finish()
