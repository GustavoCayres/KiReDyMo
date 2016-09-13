from source.chromosome import Chromosome
import sqlite3


class DatabaseSeed:

    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)

    def create_transcription_region_table(self):
        cursor = self.connection.cursor()
        cursor.executescript("""
            DROP TABLE IF EXISTS TranscriptionRegions;
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
                                              ON UPDATE CASCADE);""")
        self.connection.commit()

    def drop_transcripton_region_table(self):
        cursor = self.connection.cursor()
        cursor.executes("DROP TABLE IF EXISTS TranscriptionRegions")
        self.connection.commit()

    def import_transcription_regions(self, file_name):
        """ Imports the chromosome's transcription regions from txt file 'file_name'. """

        cursor = self.connection.cursor()

        file = open(file_name, 'r')
        for line in file:
            if line.startswith("Genomic Location(s): "):
                line_list = line.split()

                chromosome_code = line_list[2].replace(':', '')
                transcription_start = int(line_list[3].replace(',', ''))
                transcription_end = int(line_list[5].replace(',', ''))

                direction = line_list[6]
                if direction == "(-)":
                    transcription_start, transcription_end = transcription_end, transcription_start

                transcription_regions = (transcription_start, transcription_end, 30, 20, chromosome_code)
                cursor.execute("INSERT INTO TranscriptionRegions VALUES (?, ?, ?, ?, ?)", transcription_regions)

        self.connection.commit()

    def close_connection(self):
        self.connection.close()


def main():
    xml = DatabaseSeed("simulation_db.sqlite")
    xml.create_transcription_region_table()
    xml.import_transcription_regions("chromosome1.txt")
    xml.close_connection()

if __name__ == "__main__":
    main()
