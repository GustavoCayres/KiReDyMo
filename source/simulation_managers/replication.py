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

    def step(self, collision_verifier, duplication_verifier):
        if duplication_verifier.will_end(replication=self):
            self.finish()
        elif self.is_paused():  # TODO: paused don't interact
            self.advance_repairs()
        elif collision_verifier.will_collide_with_transcription(replication=self):
            self.fork_position = collision_verifier.resulting_position_after_collision(replication=self)
            self.pause()
        else:
            self.fork_position += self.speed * self.direction

    def pause(self):
        if self.origin.replication_repair_duration <= 0:
            return

        self.current_repair_wait = self.origin.replication_repair_duration
        self.speed = 0

    def finish(self):
        self.fork_position = None

    def is_active(self):
        return self.fork_position is not None

    def is_paused(self):
        return self.speed == 0

    def advance_repairs(self):
        self.current_repair_wait -= 1
        if self.current_repair_wait == 0:
            self.speed = self.origin.replication_speed
