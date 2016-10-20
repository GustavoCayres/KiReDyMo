#!/usr/bin/env python3
# Run with: python3 Trypanosoma-test_seed_script.py
from source.db_modules.database_wrapper import *
import sys

drop_tables()
create_tables()

chromosome_amount = int(sys.argv[1])

insert_chromosomes("input/Trypanosoma-cruzi/Trypanosoma-cruzi-CL-Brener-Esmeraldo-like_chromosome1.txt", 67, 2)
insert_chromosomes("input/Trypanosoma-cruzi/Trypanosoma-cruzi-CL-Brener-Esmeraldo-like_chromosome2.txt", 67, 2)
insert_replication_origin(30000, "TcChr1-S")
insert_replication_origin(30000, "TcChr2-S")

for i in range(chromosome_amount):
    index = str(i)
    file_path = "input/Trypanosoma-cruzi-CL-Brener-Esmeraldo-like_chromosome" + index + ".txt"
    file_path = "input/TcChr" + str(i) + "-S_regions.txt"
    insert_transcription_regions_from_file(file_path, 30, 150)

close()

print("Database seeded.")
