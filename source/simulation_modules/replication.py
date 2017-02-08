class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

        self.fork_position = origin.position
        self.speed = origin.replication_speed
        self.current_repair_wait = 0

    def __str__(self):
        return "Current position: " + str(self.fork_position)

    def step(self):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        if self.current_repair_wait > 0:
            self.current_repair_wait -= 1
            if self.current_repair_wait == 0:
                self.speed = self.origin.replication_speed
        else:
            self.fork_position += self.speed * self.direction

    def pause(self):
        """ Pauses the replication for a certain duration to allow repairs. """
        """ The unity added to the repair duration compensates the step taken immediately after the pause. """

        self.current_repair_wait = self.origin.replication_repair_duration + 1
        self.speed = 0

    def finish(self):
        """ Removes the replication machinery"""

        self.fork_position = None

    def is_active(self):
        return self.fork_position is not None
