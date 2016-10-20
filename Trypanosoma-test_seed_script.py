#!/usr/bin/env python3
# Run with: python3 Trypanosoma-test_seed_script.py
from source.db_modules.database_wrapper import *


drop_tables()
create_tables()
insert_chromosomes("input/Trypanosoma-test/Trypanosoma-test_chromosome1.txt", 2, 2)
insert_chromosome("TtChr2", 30, 2, 5, "Trypanosoma test")
insert_replication_origin(10, "TtChr1")
insert_replication_origin(4, "TtChr2")
insert_transcription_regions("input/Trypanosoma-test/TtChr1_regions.txt", 1, 150)
close()

print("Database up.")
