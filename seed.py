#!/usr/bin/env python3
from source.database_managers.database import Database


with Database('db/simulation.sqlite') as db:
    db.drop_tables()
    db.create_tables()

    chromosome_amount = db.insert_chromosomes(file_name="input/Tcruzi_chromosomes.txt")

    for i in range(chromosome_amount):
        index = str(i + 1)
        file_name = "input/genes/TcChr" + index + "-S_regions.txt"
        db.insert_transcription_regions(file_name=file_name, speed=30, delay=1000)
        code = "TcChr" + index + "-S"
        db.insert_replication_origins(chromosome_code=code, replication_speed=67, replication_repair_duration=20)

    db.commit()
