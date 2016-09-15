import sqlite3
from source.chromosome import Chromosome


class DatabaseImport:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def import_chromosome_by_organism(self, organism_name):

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Chromosomes WHERE Chromosomes.organism_name = ?", (organism_name,))
        result = cursor.fetchall()
        return Chromosome(result[0][0], [5], [], result[0][1], result[0][2], result[0][3])

    def close(self):
        self.connection.close()
