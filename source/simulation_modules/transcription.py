import math


class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, transcription_region):
        self.region = transcription_region
        self.current_position = transcription_region.start                 # current position of this transcription
        self.direction = math.copysign(1, self.region.end - self.region.start)
        self.speed = transcription_region.speed

    def step(self):
        """ Takes a step in this transcription, taking into account the region's boundaries. """

        self.current_position += self.direction * self.region.speed

    def finish(self):
        """ Ends this transcription. """

        self.current_position = None       # end of transcription removes the machinery

    def leaving_region(self):
        return self.direction * self.current_position + self.speed > self.direction * self.region.end
