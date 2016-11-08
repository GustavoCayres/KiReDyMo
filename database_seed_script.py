#!/usr/bin/env python3
# Run with: python3 database_seed_script.py
from source.db_modules.database_create import *
from source.db_modules.database_insert import insert_replication_origin, insert_transcription_regions_from_file, \
    insert_chromosomes_from_file

drop_tables()
create_tables()

chromosome_amount = insert_chromosomes_from_file("input/Tcruzi_chromosomes.txt", 67)
chromosome_amount = 1
for i in range(1, chromosome_amount + 1):
    index = str(i)
    file_path = "input/TcChr" + index + "-S_regions.txt"
    insert_transcription_regions_from_file(file_path, 30, 150)
    file_path = "TcChr" + index + "-S"
    # insert_replication_origin(position=0, start_probability=.2, chromosome=file_path)
    insert_replication_origin(position=10000, start_probability=.2, chromosome=file_path)


print("Database seeded.")
