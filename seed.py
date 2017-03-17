#!/usr/bin/env python3
from source.database_managers.database import Database
import os


with Database('db/simulation.sqlite') as db:
    db.drop_tables()
    db.create_tables()

    for organism_folder in os.listdir("input/organisms"):
        organism_path = "input/organisms/" + organism_folder
        chromosome_amount = db.insert_chromosomes(file_name=organism_path + "/chromosomes.txt")

        for gene_file in os.listdir(organism_path + "/genes"):
            transcription_regions_path = organism_path + "/genes/" + gene_file
            db.insert_transcription_regions(file_name=transcription_regions_path, speed=30, delay=1000)
            code = gene_file.strip("_regions.txt")
            db.insert_replication_origins(chromosome_code=code, replication_speed=67, replication_repair_duration=20)

    db.commit()
