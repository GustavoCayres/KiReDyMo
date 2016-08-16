import math

class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, transcription_region):
        self.transcription_region = transcription_region
        self.delay_wait = 0
        self.transcription_current_position = None

    def begin(self):
        """ Begins transcription in this transcription region. """

        self.transcription_current_position = self.transcription_region.transcription_start

    def step(self):
        if self.delay_wait > 0:
            self.delay_wait -= 1
            return

        # calculating the direction transcription should occur in this region
        direction = self.transcription_region.transcription_end - self.transcription_region.transcription_start
        direction = math.copysign(1, direction)

        new_position = self.transcription_current_position + (direction * self.transcription_region.speed)
        if (direction * new_position) < (direction * self.transcription_region.transcription_end):
            self.transcription_current_position = new_position
        else:
            self.transcription_current_position = self.transcription_region.transcription_end
            self.delay_wait = self.transcription_region.delay
