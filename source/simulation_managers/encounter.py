import itertools


class Encounter:
    """ Controls the encounter's between two replication machineries. """

    def __init__(self, chromosome):
        self.chromosome_length = chromosome.length

    @staticmethod
    def verify(replication1, replication2):
        """ Verifies whether there is an imminent encounter between the replications' machineries. """

        if not replication1.is_active() or not replication2.is_active() or\
                replication1.direction == replication2.direction:
            return

        if 0 < -replication1.direction * replication1.position +\
                -replication2.direction * replication2.position <= replication1.speed + replication2.speed:
            encounter_position = round((replication1.speed * replication2.position + replication2.speed *
                                        replication1.position)/(replication1.speed + replication2.speed))
            replication1.finish(encounter_position)
            replication2.finish(encounter_position)

    def resolve(self, replications):
        """ Verify encounters between all possible replication pairs. """

        for pair in itertools.combinations(replications, 2):
            self.verify(*pair)

        for replication in replications:
            if replication.is_active():
                if replication.position + replication.direction * replication.speed < 0:
                    replication.finish(0)
                elif replication.position + replication.direction * replication.speed >= self.chromosome_length:
                    replication.finish(self.chromosome_length - 1)

        replications[:] = [x for x in replications if x.is_active()]
