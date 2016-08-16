
class Simulation:
    """ Class responsible for controlling the steps of the replication process. """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.replication_origin = None
        self.replication_left_fork = None
        self.replication_right_fork = None
        self.transcriptions_current_positions = {}

    def begin_replication(self):
        """ Begin the replication process, which consists in choosing an origin and starting the transcription
         process in each transcription region. """

        self.replication_origin = self.chromosome.select_origin()
        self.replication_left_fork = self.replication_right_fork = self.replication_origin
        self.begin_transcriptions()

    def begin_transcriptions(self):
        """ Begin transcription in each transcription region. """

        for transcription_region in self.chromosome.transcription_regions:
            transcription_region.begin_transcription()
            key = transcription_region
            self.transcriptions_current_positions[key] = transcription_region.starting_base()