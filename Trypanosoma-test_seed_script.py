#!/usr/bin/env python3
# Run with: python3 Trypanosoma-test_seed_script.py


from source.db_modules.database_wrapper import *


database = Database()
database.drop_tables()
database.create_tables()
database.insert_chromosomes("input/Trypanosoma-test/Trypanosoma-test_chromosome1.txt", 2, 2)
database.insert_replication_origin(33, "TtChr1")
database.insert_transcription_regions("input/Trypanosoma-test/TtChr1_regions.txt", 1, 150)
database.close()

print("Database up.")
