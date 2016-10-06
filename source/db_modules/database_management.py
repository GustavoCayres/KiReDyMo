#!/usr/bin/env python3
from source.models.base_model import db
from source.models.chromosome import Chromosome
from source.models.transcription_region import TranscriptionRegion
from source.models.organism import Organism
from source.models.replication_origin import ReplicationOrigin


def create_tables():
    db.connect()
    db.create_tables([Chromosome, Organism, TranscriptionRegion, ReplicationOrigin], safe=True)


def drop_tables():
    db.connect()
    db.drop_tables([Chromosome, Organism, TranscriptionRegion, ReplicationOrigin])


def close():
    db.close()


def insert_organism(organism_name):
    db.connect()
    Organism.create(name=organism_name)


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
            TranscriptionRegion.create(start=start, end=end, chromosome=chromosome, speed=speed, delay=delay)

    file.close()
