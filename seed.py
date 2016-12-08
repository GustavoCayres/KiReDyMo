#!/usr/bin/env python3
from source.database_management.database import Database


with Database('db/simulation.sqlite') as db:
    db.drop_tables()
    db.create_tables()

    chromosome_amount = db.insert_chromosomes(file_name="input/Tcruzi_chromosomes.txt", replication_speed=67)

    for i in range(chromosome_amount):
        index = str(i + 1)
        file_name = "input/genes/TcChr" + index + "-S_regions.txt"
        db.insert_transcription_regions(file_name=file_name, speed=30, delay=1000)
        code = "TcChr" + index + "-S"
        db.insert_replication_origins(code)

    db.commit()

print("Database ready.")
