class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

        self.finished = False
        self.fork_position = origin.position
        self.speed = origin.replication_speed
        self.current_repair_wait = 0

    def __str__(self):
        return "Current position: " + str(self.fork_position)

    def __eq__(self, other):
        return type(self) == type(other) and self.fork_position == other.fork_position

    def __hash__(self):
        return hash(self.fork_position)

    def step(self, collision_verifier, encounter_verifier):
        previous_position = self.fork_position

        if encounter_verifier.will_end(replication=self):
            self.finished = True
            self.fork_position = encounter_verifier.resulting_position_after_finalization(replication=self)

        elif self.is_paused():  # TODO: paused don't interact
            self.advance_repairs()
        elif collision_verifier.will_collide_with_transcription(replication=self):
            self.pause()
            self.fork_position = collision_verifier.resulting_position_after_collision(replication=self)

        else:
            self.fork_position += self.speed * self.direction

        encounter_verifier.duplicate_segment(start=previous_position, end=self.fork_position)

    def pause(self):
        if self.origin.replication_repair_duration <= 0:
            return

        self.current_repair_wait = self.origin.replication_repair_duration
        self.speed = 0

    def is_paused(self):
        return self.speed == 0

    def advance_repairs(self):
        self.current_repair_wait -= 1
        if self.current_repair_wait == 0:
            self.speed = self.origin.replication_speed
