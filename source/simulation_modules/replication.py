class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, direction):
        self.speed = origin.replication_speed
        self.direction = direction
        self.fork_position = origin.position
        self.repair_wait = 0
        self.repair_duration = origin.replication_repair_duration

    def __str__(self):
        return "Current position: " + str(self.fork_position)

    def step(self):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        if self.repair_wait > 0:
            self.repair_wait -= 1
        else:
            self.fork_position += self.speed * self.direction

    def pause(self):
        """ Pauses the replication for a certain duration to allow repairs. """

        self.repair_wait = self.repair_duration + 1    # compensates the step taken after the pause

    def finish(self):
        self.fork_position = None

    def is_active(self):
        return self.fork_position is not None
