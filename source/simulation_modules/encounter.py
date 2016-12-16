import itertools


class Encounter:
    """ Controls the encounter's between two replication machineries. """

    def __init__(self, chromosome_length):
        self.chromosome_length = chromosome_length
        self.chromosome_start_done = False
        self.chromosome_end_done = False
        self.encounters = 0

    def verify(self, replication1, replication2):
        """ Verifies whether there is an imminent encounter between the replications' machineries. """

        if replication1.direction != replication2.direction and\
                abs(replication1.fork_position - replication2.fork_position) <= replication1.speed + replication2.speed:
            self.encounters += 1
            replication1.finish()
            replication2.finish()

    def resolve(self, replications):
        """ Verify encouters between all possible replication pairs. """

        for pair in itertools.combinations(replications, 2):
            Encounter.verify(*pair)

        for replication in replications:
            if replication.fork_position is not None:
                if replication.fork_position + replication.direction * replication.speed < 0:
                    self.chromosome_start_done = True
                    replication.finish()
                elif replication.fork_position + replication.direction * replication.speed >= self.chromosome_length:
                    self.chromosome_end_done = True
                    replication.finish()

        replications[:] = [x for x in replications if x.fork_position is not None]

        return self.chromosome_start_done and self.chromosome_end_done
