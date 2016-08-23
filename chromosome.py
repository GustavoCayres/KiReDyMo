from transcription_region import TranscriptionRegion


class Chromosome:
    """ Class containing data on the chromosome """
    """ Also provides basic information to the replication process. """

    def __init__(self, code, replication_origins, transcription_regions, length, replication_speed, repair_duration):
        """ A chromosome named 'code' consists of two parallel DNA strands with length 'length', therefore it has bases
        numbered from 0 to 'length'-1. """
        """ It's replication origins are integers stored in the list 'replication origins';
        It's transcription regions are classes of their own. """

        self.code = code                                        # string with chromosome's identification
        self.replication_origins = replication_origins          # array with position of the replication origins
        self.transcription_regions = transcription_regions      # array with regions of RNA transcription on the DNA
        self.length = length                                    # int with length of the chromosome
        self.replication_speed = replication_speed              # int with speed of the replication's forks
        self.repair_duration = repair_duration                  # int with the duration of pauses after head collisions

    def add_transcription_region(self, transcription_start, transcription_end, speed, delay):
        """ Marks a new transcription region in this chromosome """

        new_region = TranscriptionRegion(self.code, transcription_start, transcription_end, speed, delay)
        self.transcription_regions.append(new_region)

    def select_origin(self):
        """ Randomly selects the replication origin for the process """

        chosen_index = 0              # In the future, it'll be selected as a random variable of some distribution
        return self.replication_origins[chosen_index]
