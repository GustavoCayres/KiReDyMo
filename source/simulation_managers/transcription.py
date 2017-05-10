import math


class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, transcription_region):
        self.region = transcription_region
        self.current_position = transcription_region.start
        self.direction = math.copysign(1, self.region.end - self.region.start)
        self.speed = transcription_region.speed

    def __str__(self):
        return "Transcription at base " + str(self.current_position) + " with direction " + str(self.direction)

    def __eq__(self, other):
        return type(self) == type(other) and self.current_position == other.current_position

    def __hash__(self):
        return hash(self.current_position)

    def step(self, collision_verifier):
        if collision_verifier.will_collide_with_replication(transcription=self):
            self.finish()
        elif self.will_reach_region_end():
            self.finish()
        else:
            self.current_position += self.direction * self.region.speed

    def finish(self):
        self.current_position = None

    def will_reach_region_end(self):
        return self.direction * self.current_position + self.speed > self.direction * self.region.end

    def is_active(self):
        return self.current_position is not None
