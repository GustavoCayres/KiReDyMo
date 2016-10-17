#!/usr/bin/env python3
from source.models.base_model import db
from source.models.chromosome import Chromosome
from source.models.transcription_region import TranscriptionRegion
from source.models.replication_origin import ReplicationOrigin


def connect():
    db.connect()


def create_tables():
    db.create_tables([Chromosome, TranscriptionRegion, ReplicationOrigin], safe=True)


def drop_tables():
    db.drop_tables([Chromosome, TranscriptionRegion, ReplicationOrigin], safe=True)


def close():
    db.close()


def insert_chromosome(code, length, replication_speed, repair_duration, organism):
    Chromosome.insert(code=code, length=length, replication_speed=replication_speed,
                      repair_duration=repair_duration, organism=organism).execute()


def insert_replication_origin(position, chromosome):
    """ Insert a replication origin with the specified origin position in the specified chromosome. """
    ReplicationOrigin.insert(position=position, chromosome=chromosome).execute()


def insert_transcription_region(start, end, speed, delay, chromosome):
    TranscriptionRegion.insert(start=start, end=end, speed=speed, delay=delay, chromosome=chromosome).execute()


def get_chromosome_by_code(code):
    return Chromosome.get(Chromosome.code == code)


def get_transcription_region_by_chromosome(chromosome_code):
    return TranscriptionRegion.get(TranscriptionRegion.chromosome == chromosome_code)


def insert_transcription_regions(file_name, speed, delay):
    """ Imports the chromosome's transcription regions from txt file 'file_name'. """

    file = open(file_name, 'r')

    chromosome = ''
    end = -1
    start = -1
    speed = int(speed)
    delay = int(delay)

    for line in file:
        if line.startswith("Genomic Location(s): "):
            line_list = line.split()

            chromosome = line_list[2].replace(':', '')
            start = int(line_list[3].replace(',', ''))
            end = int(line_list[5].replace(',', ''))

            direction = line_list[6]
            if direction == "(-)":
                start, end = end, start

        elif line.startswith("--"):          # finished reading a region
            TranscriptionRegion.insert(start=start, end=end, chromosome=chromosome,
                                       speed=speed, delay=delay).execute()

    file.close()


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

# TODO: Work with wig data.
