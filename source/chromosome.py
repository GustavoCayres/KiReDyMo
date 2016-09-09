from transcription_region import TranscriptionRegion
import re


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
        self.replication_speed = replication_speed              # int with speed of the replication's forks (bases/s)
        self.repair_duration = repair_duration                  # int with the duration of pauses after head collisions

    def __str__(self):

        list_representation = list()
        list_representation.append("Chromosome: " + self.code)
        list_representation.append("Origins: " + str(self.replication_origins))
        list_representation.append("Length: " + str(self.length))
        list_representation.append("Replication Speed: " + str(self.replication_speed))
        list_representation.append("Repair Duration: " + str(self.repair_duration))
        list_representation.append("Transcription Regions: ")

        regions = ""
        for region in self.transcription_regions:

            regions += str(region)
        list_representation.append(regions)

        return "\n".join(list_representation)

    def add_transcription_region(self, transcription_start, transcription_end, speed, delay):
        """ Marks a new transcription region in this chromosome. """

        new_region = TranscriptionRegion(self.code, transcription_start, transcription_end, speed, delay)
        self.transcription_regions.append(new_region)

    def select_origin(self):
        """ Randomly selects the replication origin for the process. """

        chosen_index = 0              # In the future, it'll be selected as a random variable of some distribution
        return self.replication_origins[chosen_index]

    # ongoing
    def add_origins(self, file_name):
        """ Adds replication origins to this chromosome from a .wig file. """

        file = open(file_name, 'r')
        origin_value =
        should_read_values = False
        for line in file:
            reg = re.search('(?<=chrom=)\w+', line)
            if reg is not None:
                if reg.group(0) == self.code:
                    should_read_values = True
                else:
                    should_read_values = False
            elif should_read_values:

        if wig_header is None:
            print("Chromosome code not found in .wig file.")
            return
