import math


class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, transcription_region):
        self.region = transcription_region
        self.delay_wait = 0
        self.current_position = None

    def begin(self):
        """ Begins transcription in this transcription region. """

        self.current_position = self.region.transcription_start

    def step(self):
        """ Takes a step in this transcription, taking into account the region's boundaries. """

        if self.delay_wait > 0:
            self.delay_wait -= 1
            if self.delay_wait == 0:
                self.current_position = self.region.transcription_start
            return

        # calculating the direction transcription should occur in this region
        direction = self.region.transcription_end - self.region.transcription_start
        direction = math.copysign(1, direction)

        new_position = self.current_position + (direction * self.region.speed)
        if (direction * new_position) < (direction * self.region.transcription_end):
            self.current_position = new_position
        else:
            self.current_position = None    # end of transcription removes the machinery
            self.delay_wait = self.region.delay
