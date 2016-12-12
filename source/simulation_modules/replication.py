class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, replication_speed, repair_duration):
        self.speed = replication_speed
        self.left_fork = origin.position
        self.right_fork = origin.position
        self.left_repair_wait = 0
        self.right_repair_wait = 0
        self.repair_duration = repair_duration

    def step(self, current_step):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        if self.left_fork is not None:
            if self.left_repair_wait > 0:
                self.left_repair_wait -= 1
            else:
                self.left_fork -= self.speed

        if self.right_fork is not None:
            if self.right_repair_wait > 0:
                self.right_repair_wait -= 1
            else:
                self.right_fork += self.speed

    def pause(self, fork):
        """ Pauses the replication for a certain duration to allow repairs. """

        if fork == "left":
            self.left_repair_wait = self.repair_duration + 1    # compensates the step taken after the pause
        else:
            self.right_repair_wait = self.repair_duration + 1
