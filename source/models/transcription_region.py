class TranscriptionRegion:
    """ Model of each transcription region """

    def __init__(self, start, end, speed, delay):
        self.start = start
        self.end = end
        self.speed = speed
        self.delay = delay

    def __str__(self):
        return "(" + str(self.start) + ", " + str(self.end) + ")"
