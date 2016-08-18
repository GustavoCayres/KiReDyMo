import math


class Transcription:
    """ Controls the transcription process of a specific region. """

    def __init__(self, transcription_region):
        self.region = transcription_region
        self.delay_wait = 0                                 # remaining time to wait the delay of this transcription
        self.current_position = None                        # current position of this transcription
        self.direction = math.copysign(1, self.region.transcription_end - self.region.transcription_start)

    def begin(self):
        """ Begins transcription in this transcription region. """

        self.current_position = self.region.transcription_start

    def step(self):
        """ Takes a step in this transcription, taking into account the region's boundaries. """

        if self.delay_wait > 0:
            self.delay_wait -= 1
            if self.delay_wait == 0:
                self.begin()
            return

        new_position = self.current_position + (self.direction * self.region.speed)
        if (self.direction * new_position) < (self.direction * self.region.transcription_end):
            self.current_position = new_position
        else:
            self.finish()
            self.delay_wait -= 1

    def finish(self):
        """ Ends this transcription and starts the countdown for restart. """

        self.current_position = None       # end of transcription removes the machinery
        self.delay_wait = self.region.delay + 1       # compensates the step taken after the end

