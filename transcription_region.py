class TranscriptionRegion:
    """ Organizes the properties of each transcript region,
        allowing different transcription speeds for each transcription region. """
    """ Also controls the transcription process """

    def __init__(self, chromosome_code, coordinates, speed, delay):
        self.chromosome_code = chromosome_code  # identification of the chromosome that contains this region
        self.coordinates = coordinates          # tuple with the coordinates of the transcription's beginning and end
        self.speed = speed                      # speed of transcription (in bases per second)
        self.delay = delay                      # time between consecutive transcriptions in this region

    def starting_base(self):
        """ Returns the starting base of the transcription in this region. """

        return self.coordinates[0]
