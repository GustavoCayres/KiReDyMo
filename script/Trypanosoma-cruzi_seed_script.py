#!/usr/bin/env python3
# Run with: python3 -m input.Trypanosoma-cruzi.Trypanosoma-cruzi_seed_script

import sys

from source.db_modules.database_wrapper import DatabaseCreate


def main(database_name):
    db = DatabaseCreate(database_name)
    db.drop_tables()
    db.create_tables()
    db.insert_organism("T. cruzi CL Brener Esmeraldo-like")
    db.insert_chromosomes("input/Trypanosoma-cruzi/Trypanosoma-cruzi-CL-Brener-Esmeraldo-like_chromosome1.txt", 67, 2)
    db.insert_replication_origin(30000, "TcChr1-S")
    db.insert_transcription_regions("input/Trypanosoma-cruzi/TcChr1-S_regions.txt", 30, 150)
    db.close()
    print("Database seeded.")

if __name__ == '__main__':
    main(sys.argv[1])
