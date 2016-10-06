import math


class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, transcription_region):
        self.region = transcription_region
        self.delay_wait = 0                                 # remaining time to wait the delay of this transcription
        self.current_position = None                        # current position of this transcription
        self.direction = math.copysign(1, self.region.end - self.region.start)

    def begin(self):
        """ Begins transcription in this transcription region. """

        self.current_position = self.region.start

    def step(self):
        """ Takes a step in this transcription, taking into account the region's boundaries. """

        if self.wait_during_delay():
            return

        new_position = self.current_position + (self.direction * self.region.speed)

        # If the transcription did not reach the region's boundaries.
        if (self.direction * new_position) < (self.direction * self.region.end):
            self.current_position = new_position
        # Else, the transcription is over.
        else:
            self.finish()

    def wait_during_delay(self):
        """ Decreases the delay until the transcription restarts. Also restarts it when the delay is over. """

        if self.delay_wait > 0:
            self.delay_wait -= 1
            return True
        # Else, there is no more delay and the transcription should begin if it's not already running.
        elif self.current_position is None:
            self.begin()
            return True

        return False

    def finish(self):
        """ Ends this transcription and starts the countdown for restart. """

        self.current_position = None       # end of transcription removes the machinery
        self.delay_wait = self.region.delay

    def collapse(self):
        """ Ends this transcription due to a collision. """

        self.current_position = None
        self.delay_wait = self.region.delay + 1
