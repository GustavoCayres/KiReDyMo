#!/usr/bin/env python3
from source.database_managers.database import Database
import os


with Database('db/simulation.sqlite') as db:
    db.drop_tables()
    db.create_tables()

    for organism_folder in os.listdir("input/organisms"):
        organism_path = "input/organisms/" + organism_folder
        for text_file in os.listdir(organism_path):
            if text_file.endswith(".txt"):
                chromosome_amount = db.insert_chromosomes(file_name=organism_path + "/" + text_file)

        #for gene_file in os.listdir(organism_path + "/genes"):
         #   transcription_region_path = organism_path + "/genes/" + gene_file
         #   db.insert_transcription_regions(file_name=transcription_region_path, speed=30, delay=1000)
        for origin_file in os.listdir(organism_path + "/origins"):
            replication_origin_path = organism_path + "/origins/" + origin_file
            db.insert_replication_origins(file_name=replication_origin_path,
                                          replication_speed=67, replication_repair_duration=20)

    db.commit()
