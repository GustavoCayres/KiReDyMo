import itertools


class Encounter:
    """ Controls the encounter's between two replication machineries. """

    @staticmethod
    def verify(replication1, replication2):
        """ Verifies whether there is an imminent encounter between the replications' machineries. """
        
        replication_speed = replication1.chromosome.replication_speed
        if replication1.left_fork is not None and replication2.right_fork is not None:
            if 0 < replication1.left_fork - replication2.right_fork <= 2*replication_speed:
                replication1.left_fork = None
                replication2.right_fork = None
                print("Replication Encounter!!")
        if replication1.right_fork is not None and replication2.left_fork is not None:
            if 0 < replication2.left_fork - replication1.right_fork <= 2*replication_speed:
                replication1.right_fork = None
                replication2.left_fork = None
                print("Replication Encounter!!")

    @staticmethod
    def resolve(replications):
        """ Verify all possible replication pairs. """
        # TODO: Point of possible optimization
        if len(replications) > 1:
            Encounter.verify(replications[0], replications[1])
