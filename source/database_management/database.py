import sqlite3

from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion
from source.database_management.origin_generation import *


class Database:
    def __init__(self, database_path):
        self.db = sqlite3.connect(database_path)

    def commit(self):
        self.db.commit()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.db.close()

    def create_tables(self):
        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE Chromosome
                        (code text, length integer not null, organism text,
                        PRIMARY KEY (code, organism))''')
        cursor.execute('''CREATE TABLE ReplicationOrigin
                        (position integer, start_probability real not null,
                        replication_speed integer not null, replication_repair_duration integer not null,
                        chromosome_code text, chromosome_organism text,
                        PRIMARY KEY (position, chromosome_code, chromosome_organism)
                        FOREIGN KEY (chromosome_code, chromosome_organism) REFERENCES Chromosome(code, organism))''')
        cursor.execute('''CREATE TABLE TranscriptionRegion
                        (start integer, end integer, speed integer not null, delay integer not null,
                        chromosome_code text, chromosome_organism text,
                        PRIMARY KEY (start, end, chromosome_code, chromosome_organism)
                        FOREIGN KEY (chromosome_code, chromosome_organism) REFERENCES Chromosome(code, organism))''')

    def drop_tables(self):
        cursor = self.db.cursor()
        cursor.execute('''DROP TABLE IF EXISTS Chromosome''')
        cursor.execute('''DROP TABLE  IF EXISTS ReplicationOrigin''')
        cursor.execute('''DROP TABLE  IF EXISTS TranscriptionRegion''')

    def insert_chromosomes(self, file_name):
        """ Imports the chromosomes from txt file 'file_name'.
            The file format contain columns with headers [Length], [Description] and [Sequence ID]
            where the separation are TABs.                                                          """

        cursor = self.db.cursor()

        with open(file_name, 'r') as file:
            header_line_as_list = next(file).split("\t")
            code_index = -1         # let's find what column holds our desired data
            length_index = -1
            organism_index = -1
            for index, tag in enumerate(header_line_as_list):
                if tag == "[Length]":
                    length_index = index
                elif tag == "[Sequence ID]":
                    code_index = index
                elif tag == "[Description]":
                    organism_index = index

            chromosomes = []
            for line in file:
                line_as_list = line.split("\t")
                length = line_as_list[length_index].replace(',', '')
                code = line_as_list[code_index]
                organism = line_as_list[organism_index]
                chromosomes.append((code, length, organism))

        cursor.executemany('''INSERT INTO Chromosome VALUES (?, ?, ?)''', chromosomes)
        return len(chromosomes)

    def insert_replication_origins(self, chromosome_code, replication_speed, replication_repair_duration):
        """ Insert a replication origin with the specified
        {position, start_probability, chromosome}
        into the specified chromosome. """

        chromosome = self.select_chromosomes(code=chromosome_code)[0]
        origins = generate_origins(chromosome, replication_speed, replication_repair_duration)

        self.db.cursor().executemany('''INSERT INTO ReplicationOrigin VALUES (?, ?, ?, ?, ?, ?)''', origins)
        return len(origins)

    def insert_transcription_regions(self, file_name, speed, delay):
        """ Imports the chromosome's transcription regions from txt file 'file_name'.
            The file format must be:
            [Gene ID]   [Transcript ID] [Organism]  [Genomic Location(s)]
            where the separation are TABs.                                            """

        cursor = self.db.cursor()

        genes = []
        with open(file_name, 'r') as file:
            header_line_as_list = next(file).split("\t")
            region_index = -1               # let's find what column holds the region data
            organism_index = -1             # let's find what column holds the organism data
            for index, tag in enumerate(header_line_as_list):
                if tag == "[Genomic Location(s)]":
                    region_index = index
                elif tag == "[Organism]":
                    organism_index = index

            for line in file:
                line_as_list = line.split("\t")
                region = line_as_list[region_index].split()
                organism = line_as_list[organism_index]

                chromosome = region[0].replace(':', '')
                start = region[1].replace(',', '')
                end = region[3].replace(',', '')
                direction = region[4]
                genes.append((int(start), int(end), int(speed), int(delay), chromosome, organism, direction))

        regions = Database.convert_genes_to_regions(genes)
        cursor.executemany('''INSERT INTO TranscriptionRegion VALUES (?, ?, ?, ?, ?, ?)''',
                           regions)
        return len(regions)

    @staticmethod
    def convert_genes_to_regions(genes):
        """ Converts a list of genes to a list of polycistronic regions. """

        genes.sort(key=lambda x: x[0])
        genes.append((None, None, None, None, None, None))  # stop gene
        regions = []

        previous_gene = genes[0]
        region_start = previous_gene[0]
        region_end = previous_gene[1]
        for gene in genes[1:]:
            if previous_gene[-1] != gene[-1]:  # different polycistronic region
                start = region_start
                end = region_end
                speed = previous_gene[2]
                delay = previous_gene[3]
                chromosome_code = previous_gene[4]
                chromosome_organism = previous_gene[5]
                if previous_gene[-1] == "(-)":
                    start, end = region_end, region_start
                regions.append((start, end, speed, delay, chromosome_code, chromosome_organism))
                region_start = gene[0]

            region_end = gene[1]  # update region's end
            previous_gene = gene

        return regions

    def select_chromosomes(self, **kwargs):
        cursor = self.db.cursor()
        for key, value in kwargs.items():
            query = "SELECT * FROM Chromosome WHERE " + key + " = ?"
            cursor.execute(query, (value,))
        chromosomes = [Chromosome(code=t[0], length=t[1], organism=t[2]) for t in cursor.fetchall()]

        for chromosome in chromosomes:
            cursor.execute('''SELECT *
                              FROM ReplicationOrigin
                              WHERE chromosome_code = ? AND chromosome_organism = ?''',
                           (chromosome.code, chromosome.organism))
            chromosome.replication_origins = [ReplicationOrigin(position=t[0],
                                                                start_probability=t[1], replication_speed=t[2],
                                                                replication_repair_duration=t[3])
                                              for t in cursor.fetchall()]

            cursor.execute('''SELECT *
                              FROM TranscriptionRegion
                              WHERE chromosome_code = ? AND chromosome_organism = ?''',
                           (chromosome.code, chromosome.organism))
            chromosome.transcription_regions = [TranscriptionRegion(start=t[0], end=t[1], speed=t[2], delay=t[3])
                                                for t in cursor.fetchall()]

        return chromosomes

    def print_organisms(self):
        cursor = self.db.cursor()
        cursor.execute('''SELECT DISTINCT organism
                          FROM Chromosome''')

        print("\nOrganisms currently in the database are:")
        for organism in cursor.fetchall():
            print("\t" + str(organism[0]))
