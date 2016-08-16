class TranscriptionRegion:
    """ Organizes the properties of each transcript region,
        allowing different transcription speeds for each transcription region. """
    """ Also controls the transcription process. """

    def __init__(self, chromosome_code, transcription_start, transcription_end, speed, delay):
        self.chromosome_code = chromosome_code            # identification of the chromosome that contains this region
        self.transcription_start = transcription_start    # coordinate of the transcription's beginning
        self.transcription_end = transcription_end        # coordinate of the transcription's end
        self.speed = speed                                # speed of transcription (in bases per second)
        self.delay = delay                                # time between consecutive transcriptions in this region

    def starting_point(self):
        """ Returns the starting base of the transcription in this region. """

        return self.transcription_start

    def transcription_speed(self):
        """ Speed of the transcription process, taking in account the direction of the movement. """

        speed = self.speed
        if self.transcription_start > self.transcription_end:
            speed *= -1
        return speed
