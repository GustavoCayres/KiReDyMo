#!/usr/bin/env python3
# Run with: python3 -m input.Trypanosoma-cruzi.Trypanosoma-cruzi_seed_script
from source.db_modules.database_wrapper import *


drop_tables()
create_tables()
insert_chromosomes("input/Trypanosoma-cruzi/Trypanosoma-cruzi-CL-Brener-Esmeraldo-like_chromosome1.txt", 67, 2)
insert_replication_origin(30000, "TcChr1-S")
insert_transcription_regions("input/Trypanosoma-cruzi/TcChr1-S_regions.txt", 30, 150)
close()

print("Database seeded.")
