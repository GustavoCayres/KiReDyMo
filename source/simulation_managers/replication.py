class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, direction, strand):
        self.origin = origin
        self.direction = direction
        self.dna_strand = strand

        self.fork_position = origin.position
        self.speed = origin.replication_speed
        self.current_repair_wait = 0

    def __str__(self):
        return "Current position: " + str(self.fork_position)

    def step(self):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        previous_position = self.fork_position

        if self.current_repair_wait > 0:
            self.current_repair_wait -= 1
            if self.current_repair_wait == 0:
                self.speed = self.origin.replication_speed
        else:
            self.fork_position += self.speed * self.direction

        self.dna_strand.duplicate_segment(previous_position, self.fork_position)

    def pause(self, position):
        """ Pauses the replication for a certain duration to allow repairs. """

        if self.origin.replication_repair_duration > 0:
            previous_position = self.fork_position
            self.dna_strand.duplicate_segment(previous_position, position)
            self.fork_position = position
            self.current_repair_wait = self.origin.replication_repair_duration
            self.speed = 0

    def finish(self, final_position):
        """ Removes the replication machinery. """

        previous_position = self.fork_position
        self.dna_strand.duplicate_segment(previous_position, final_position)
        self.fork_position = None

    def is_active(self):
        return self.fork_position is not None
