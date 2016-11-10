import random


class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, repair_duration):
        self.chromosome = origin.chromosome
        self.origin = origin
        self.triggered = False
        self.left_fork = None
        self.right_fork = None
        self.left_repair_wait = 0
        self.right_repair_wait = 0
        self.repair_duration = repair_duration

    def trigger_origin(self, current_step):
        if not self.triggered:
            if random.random() < self.origin.start_probability:
                self.triggered = True
                print("Origin at position " + str(self.origin.position) + " activated at " + str(current_step))
                return self.origin.position, self.origin.position
        return self.left_fork, self.right_fork

    def step(self, current_step):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        self.left_fork, self.right_fork = self.trigger_origin(current_step)

        if self.left_fork is not None:
            if self.left_repair_wait > 0:
                self.left_repair_wait -= 1
            else:
                self.left_fork -= self.chromosome.replication_speed
                if self.left_fork < 0:                                    # verifies if the left replication ended
                    self.left_fork = None

        if self.right_fork is not None:
            if self.right_repair_wait > 0:
                self.right_repair_wait -= 1
            else:
                self.right_fork += self.chromosome.replication_speed
                if self.right_fork >= self.chromosome.length:             # verifies if the right replication ended
                    self.right_fork = None

    def pause(self, fork):
        """ Pauses the replication for a certain duration to allow repairs. """

        if fork == "left":
            self.left_repair_wait = self.repair_duration + 1    # compensates the step taken after the pause
        else:
            self.right_repair_wait = self.repair_duration + 1
