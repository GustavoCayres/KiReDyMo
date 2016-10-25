#!/usr/bin/env python3
# Run with: python3 database_seed_script.py
import sys

from source.db_modules.database_create import *
from source.db_modules.database_insert import insert_replication_origin, insert_transcription_regions_from_file, \
    insert_chromosomes

drop_tables()
create_tables()

chromosome_amount = int(sys.argv[1])

for i in range(1, chromosome_amount + 1):
    index = str(i)
    file_path = "input/Trypanosoma-cruzi-CL-Brener-Esmeraldo-like_chromosome" + index + ".txt"
    insert_chromosomes(file_path, 67, 2)
    file_path = "input/TcChr" + index + "-S_regions.txt"
    insert_transcription_regions_from_file(file_path, 30, 150)
    file_path = "TcChr" + index + "-S"
    insert_replication_origin(0, file_path)

print("Database seeded.")
