import itertools
from source.simulation_modules.completition import Completition


class Encounter:
    """ Controls the encounter's between two replication machineries. """

    def __init__(self, chromosome):
        self.chromosome_length = chromosome.length
        self.number_of_origins = len(chromosome.replication_origins)
        self.chromosome_start_done = False
        self.chromosome_end_done = False
        self.encounters = 0
        self.completition_manager = Completition()

    def verify(self, replication1, replication2):
        """ Verifies whether there is an imminent encounter between the replications' machineries. """

        if not replication1.is_active() or not replication2.is_active() or\
                replication1.direction == replication2.direction:
            return

        if 0 < -replication1.direction * replication1.fork_position +\
                -replication2.direction * replication2.fork_position <= replication1.speed + replication2.speed:
            self.completition_manager.save_replication_encountering_replication(replication1, replication2)
            self.encounters += 1
            replication1.finish()
            replication2.finish()

    def resolve(self, replications):
        """ Verify encouters between all possible replication pairs. """

        for pair in itertools.combinations(replications, 2):
            self.verify(*pair)

        for replication in replications:
            if replication.is_active():
                if replication.fork_position + replication.direction * replication.speed < 0:
                    self.completition_manager.save_replication_encountering_end(replication)
                    replication.finish()
                elif replication.fork_position + replication.direction * replication.speed >= self.chromosome_length:
                    self.completition_manager.save_replication_encountering_end(replication)
                    replication.finish()

        replications[:] = [x for x in replications if x.is_active()]

        return self.completition_manager.done()
