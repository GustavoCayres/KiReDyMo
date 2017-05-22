class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, direction, speed, repair_duration, strand):
        self.origin_position = origin.position
        self.base_speed = speed
        self.repair_duration = repair_duration
        self.direction = direction
        self.dna_strand = strand

        self.position = self.origin_position
        self.speed = self.base_speed
        self.elapsed_repair_time = 0

    def __str__(self):
        return "Current position: " + str(self.position)

    def step(self):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        previous_position = self.position

        if self.elapsed_repair_time > 0:
            self.elapsed_repair_time -= 1
            if self.elapsed_repair_time == 0:
                self.speed = self.base_speed
        else:
            self.position += self.speed * self.direction

        self.dna_strand.duplicate_segment(previous_position, self.position)

    def pause(self, position):
        """ Pauses the replication for a certain duration to allow repairs. """

        if self.repair_duration > 0:
            previous_position = self.position
            self.dna_strand.duplicate_segment(previous_position, position)
            self.position = position
            self.elapsed_repair_time = self.repair_duration
            self.speed = 0

    def finish(self, final_position):
        """ Removes the replication machinery. """

        previous_position = self.position
        self.dna_strand.duplicate_segment(previous_position, final_position)
        self.position = None

    def is_active(self):
        return self.position is not None
