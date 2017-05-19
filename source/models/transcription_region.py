class TranscriptionRegion:
    """ Model of each transcription region """

    def __init__(self, start, end, chromosome):
        self.start = start
        self.end = end
        self.speed = chromosome.transcription_speed
        self.delay = chromosome.transcription_start_delay

    def __str__(self):
        return "(" + str(self.start) + ", " + str(self.end) + ")"
