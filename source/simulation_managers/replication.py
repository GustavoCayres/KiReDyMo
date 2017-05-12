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

    def step(self, strand):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        last_position = self.fork_position

        if self.current_repair_wait > 0:
            self.current_repair_wait -= 1
            if self.current_repair_wait == 0:
                self.speed = self.origin.replication_speed
        else:
            self.fork_position += self.speed * self.direction

        strand.duplicate_segment(last_position, self.fork_position)

    def pause(self):
        """ Pauses the replication for a certain duration to allow repairs. """

        self.current_repair_wait = self.origin.replication_repair_duration
        if self.origin.replication_repair_duration > 0:
            self.speed = 0

    def finish(self, final_position, strand):
        """ Removes the replication machinery. """

        previous_position = self.fork_position
        strand.duplicate_segment(previous_position, final_position)
        self.fork_position = None

    def is_active(self):
        return self.fork_position is not None
