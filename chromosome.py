from .transcription_region import TranscriptionRegion


class Chromosome:
    """ Class containing data on the chromosome """
    """ Also controls the basic functions of the replication process. """

    def __init__(self, code, replication_origins, transcription_regions, length):
        """ A chromosome named 'code' consists of two parallel DNA strands with length 'length', therefore it has bases
        numbered from 0 to 'length'-1. """
        """ It's replication origins are tuples of 2 integers stored in the list 'replication origins';
         the first integer represents the position of first base, whereas the last integer represents the position of
         the last base + 1.
        It's transcription regions are objects stored in the same way as the replication origins. """

        self.code = code                                        # chromosome's identification
        self.replication_origins = replication_origins          # position of the replication origins
        self.transcription_regions = transcription_regions      # regions of RNA transcription on the DNA
        self.length = length                                    # length of the chromosome

    def add_transcription_region(self, coordinates, speed, delay):
        """ Marks a new transcription region in this chromosome """

        new_region = TranscriptionRegion(self.code, coordinates, speed, delay)
        self.transcription_regions.append(new_region)

    def select_origin(self):
        """ Randomly selects the replication origin for the process """

        chosen_index = 0              # In the future, it'll be selected as a random variable of some distribution
        return self.replication_origins[chosen_index]
