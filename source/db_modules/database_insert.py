from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion


def insert_chromosome(code, length, replication_speed, repair_duration, organism):
    Chromosome.insert(code=code, length=length, replication_speed=replication_speed,
                      repair_duration=repair_duration, organism=organism).execute()


def insert_replication_origin(position, chromosome):
    """ Insert a replication origin with the specified origin position in the specified chromosome. """
    ReplicationOrigin.insert(position=position, chromosome=chromosome).execute()


def insert_transcription_region(start, end, speed, delay, chromosome):
    TranscriptionRegion.insert(start=start, end=end, speed=speed, delay=delay, chromosome=chromosome).execute()


def insert_transcription_regions_from_file(file_name, speed, delay):
    """ Imports the chromosome's transcription regions from txt file 'file_name'.
        The file format must be:
        [Gene ID]   [Transcript ID] [Organism]  [Genomic Location(s)]
        where the separation are TABs.                                            """

    with open(file_name, 'r') as file:
        header_line_as_list = next(file).split("\t")
        data_index = -1                 # let's find what column holds our desired data
        for index, tag in enumerate(header_line_as_list):
            if tag == "[Genomic Location(s)]":
                data_index = index

        for line in file:
            line_as_list = line.split("\t")
            data = line_as_list[data_index].split()

            chromosome = data[0].replace(':', '')
            start = int(data[1].replace(',', ''))
            end = int(data[3].replace(',', ''))
            direction = data[4]
            if direction == "(-)":
                start, end = end, start

            TranscriptionRegion.insert(start=start, end=end, chromosome=chromosome, speed=int(speed), delay=int(delay))\
                .execute()


def insert_chromosomes(file_name, replication_speed, repair_duration):
    """ Imports the chromosomes from txt file 'file_name'. """

    file = open(file_name, 'r')

    code = ''
    length = -1
    organism = ''
    replication_speed = int(replication_speed)
    repair_duration = int(repair_duration)

    for line in file:
        if line.startswith("Sequence ID: "):
            line_list = line.split(': ')
            code = line_list[1].strip('\n')

        elif line.startswith("Length: "):
            line_list = line.split()
            length = int(line_list[1].replace(',', ''))

        elif line.startswith("Organism: "):
            line_list = line.split(' ', 1)
            organism = line_list[1].strip('\n')

        elif line.startswith("--"):  # finished reading a chromosome
            Chromosome.insert(code=code, length=length, replication_speed=replication_speed,
                              repair_duration=repair_duration, organism=organism).execute()

    file.close()
