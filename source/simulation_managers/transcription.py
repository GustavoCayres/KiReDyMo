import math


class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, region, speed):
        self.region = region
        self.direction = math.copysign(1, self.region.end - self.region.start)
        self.speed = speed

        self.position = region.start

    def step(self):
        """ Takes a step in this transcription. """

        self.position += self.direction * self.speed

    def finish(self):
        """ Ends this transcription, removing the machinery. """

        self.position = None

    def is_leaving_region(self):
        return self.direction * self.position + self.speed > self.direction * self.region.end

    def is_active(self):
        return self.position is not None
