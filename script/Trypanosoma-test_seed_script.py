#!/usr/bin/env python3
# Run with: python3 -m input.Trypanosoma-test.Trypanosoma-test_seed_script 'db/simulation_db.sqlite'

from source.db_modules.database_seed import DatabaseSeed
import sys


def main(database_name):
    db = DatabaseSeed(database_name)
    db.drop_tables()
    db.create_tables()
    db.insert_organism("Trypanosoma test")
    db.insert_chromosomes("input/Trypanosoma-test/Trypanosoma-test_chromosome1.txt", 2, 2)
    db.insert_replication_origins(10, "TtChr1")
    db.insert_transcription_regions("input/Trypanosoma-test/TtChr1_regions.txt", 1, 150)
    db.close()
    print("Database seeded.")

if __name__ == "__main__":
    main(sys.argv[1])
