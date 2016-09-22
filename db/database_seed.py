#!/usr/bin/env python3
import sqlite3


class DatabaseSeed:

    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.executescript("""
            CREATE TABLE Organisms (
                name VARCHAR (30) PRIMARY KEY
            );

            CREATE TABLE Chromosomes (
                code              VARCHAR (10) PRIMARY KEY,
                length            INTEGER,
                replication_speed INTEGER,
                repair_duration   INTEGER,
                organism_name     VARCHAR (30) REFERENCES Organisms (name) ON DELETE RESTRICT
                                                               ON UPDATE CASCADE
            );

            CREATE TABLE ReplicationOrigins (
                origin          INTEGER,
                chromosome_code VARCHAR (10) NOT NULL,
                FOREIGN KEY (
                    chromosome_code
                )
                REFERENCES Chromosomes (code) ON DELETE CASCADE
                                            ON UPDATE CASCADE,
                PRIMARY KEY (
                    origin,
                    chromosome_code
                )
            );

            CREATE TABLE TranscriptionRegions (
                transcription_start INTEGER,
                transcription_end   INTEGER,
                speed               INTEGER,
                delay               INTEGER,
                chromosome_code     VARCHAR (10),
                PRIMARY KEY (
                    transcription_start,
                    transcription_end,
                    chromosome_code
                ),
                FOREIGN KEY (
                    chromosome_code
                )
                REFERENCES Chromosomes (code) ON DELETE CASCADE
                                              ON UPDATE CASCADE
            );""")

    def drop_tables(self):
        cursor = self.connection.cursor()
        cursor.executescript("""
                    DROP TABLE IF EXISTS TranscriptionRegions;
                    DROP TABLE IF EXISTS Organisms;
                    DROP TABLE IF EXISTS ReplicationOrigins;
                    DROP TABLE IF EXISTS Chromosomes;""")

    def insert_organism(self, organism_name):
        """ Insert an organism with the specified name. """

        cursor = self.connection.cursor()

        organism = (organism_name,)
        cursor.execute("INSERT INTO Organisms VALUES (?)", organism)

    def insert_transcription_regions(self, file_name, speed, delay):
        """ Imports the chromosome's transcription regions from txt file 'file_name'. """

        cursor = self.connection.cursor()
        file = open(file_name, 'r')

        chromosome_code = ''
        transcription_end = -1
        transcription_start = -1
        speed = int(speed)
        delay = int(delay)

        for line in file:
            if line.startswith("Genomic Location(s): "):
                line_list = line.split()

                chromosome_code = line_list[2].replace(':', '')
                transcription_start = int(line_list[3].replace(',', ''))
                transcription_end = int(line_list[5].replace(',', ''))

                direction = line_list[6]
                if direction == "(-)":
                    transcription_start, transcription_end = transcription_end, transcription_start

            elif line.startswith("--"):                         # finished reading a region
                transcription_region = (transcription_start, transcription_end, speed, delay, chromosome_code)
                cursor.execute("INSERT INTO TranscriptionRegions VALUES (?, ?, ?, ?, ?)", transcription_region)

        file.close()

    def insert_chromosomes(self, file_name, replication_speed, repair_duration):
        """ Imports the chromosomes from txt file 'file_name'. """

        cursor = self.connection.cursor()
        file = open(file_name, 'r')

        code = ''
        length = -1
        organism_name = ''
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
                organism_name = line_list[1].strip('\n')

            elif line.startswith("--"):            # finished reading a chromosome
                chromosome = (code, length, replication_speed, repair_duration, organism_name)
                cursor.execute("INSERT INTO Chromosomes VALUES (?, ?, ?, ?, ?)", chromosome)

        file.close()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def insert_replication_origins(self, origin, chromosome_code):
        """ Insert a replication origin with the specified origin position in the specified chromosome. """

        cursor = self.connection.cursor()

        replication_origin = (int(origin), chromosome_code)
        cursor.execute("INSERT INTO ReplicationOrigins VALUES (?, ?)", replication_origin)
