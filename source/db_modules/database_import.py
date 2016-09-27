import sqlite3
from source.simulation_modules.chromosome import Chromosome
from source.simulation_modules.transcription_region import TranscriptionRegion


class DatabaseImport:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def import_origins_by_chromosome(self, chromosome_code):
        cursor = self.connection.cursor()
        cursor.execute("SELECT origin FROM ReplicationOrigins WHERE chromosome_code = ?", (chromosome_code,))
        origins = cursor.fetchall()             # fetch origins from database

        for i in range(len(origins)):           # convert to a conventional list
            origins[i] = origins[i][0]

        return origins

    def import_regions_by_chromosome(self, chromosome_code):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM TranscriptionRegions WHERE chromosome_code = ?", (chromosome_code,))
        regions = cursor.fetchall()  # fetch origins from database

        for i in range(len(regions)):  # convert to a conventional list
            regions[i] = TranscriptionRegion(regions[i][0], regions[i][1], regions[i][2], regions[i][3])

        return regions

    # TODO: Allow import of multiple chromosomes.
    def import_chromosome_by_organism(self, organism_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Chromosomes WHERE Chromosomes.organism_name = ?", (organism_name,))
        chromosome = cursor.fetchall()

        code = chromosome[0][0]
        replication_origins = self.import_origins_by_chromosome(code)
        transcription_regions = self.import_regions_by_chromosome(code)
        length = chromosome[0][1]
        replication_speed = chromosome[0][2]
        repair_duration = chromosome[0][3]

        return Chromosome(code, replication_origins, transcription_regions, length, replication_speed, repair_duration)

    def close(self):
        self.connection.close()
