import itertools

from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.replication import Replication


class Encounter:
    """ Controls the encounter's between two replication machineries. """

    def __init__(self, chromosome_length):
        self.chromosome_start = Replication(ReplicationOrigin(0, None, 0, None))
        self.chromosome_end = Replication(ReplicationOrigin(chromosome_length - 1, None, 0, None))

    @staticmethod
    def verify(replication1, replication2):
        """ Verifies whether there is an imminent encounter between the replications' machineries. """

        if replication1.left_fork is not None and replication2.right_fork is not None:
            if 0 < replication1.left_fork - replication2.right_fork <= replication1.speed + replication2.speed:
                # print("Encounter between replication machineries around base " + str(replication1.left_fork))
                replication1.left_fork = None
                replication2.right_fork = None

        if replication1.right_fork is not None and replication2.left_fork is not None:
            if 0 < replication2.left_fork - replication1.right_fork <= replication1.speed + replication2.speed:
                # print("Encounter between replication machineries around base " + str(replication1.right_fork))
                replication1.right_fork = None
                replication2.left_fork = None

    def resolve(self, replications):
        """ Verify encouters between all possible replication pairs. """

        replications_with_borders = replications[:]
        replications_with_borders.append(self.chromosome_start)
        replications_with_borders.append(self.chromosome_end)
        for pair in itertools.combinations(replications_with_borders, 2):
            Encounter.verify(*pair)

        self.chromosome_start = replications_with_borders[-2]
        self.chromosome_end = replications_with_borders[-1]
        if self.chromosome_start.right_fork is None and self.chromosome_end.left_fork is None:
            return True
        return False
