class TranscriptionRegion:
    """ Organizes the properties of each transcript region,
        allowing different transcription speeds for each transcription region. """
    """ Also controls the transcription process. """

    def __init__(self, transcription_start, transcription_end, speed, delay):
        self.transcription_start = transcription_start    # coordinate of the transcription's beginning
        self.transcription_end = transcription_end        # coordinate of the transcription's end (closed interval)
        self.speed = speed                                # speed of transcription (in bases per second)
        self.delay = delay                                # time between consecutive transcriptions in this region

    def __str__(self):
        return "(" + str(self.transcription_start) + ", " + str(self.transcription_end) + ")"
