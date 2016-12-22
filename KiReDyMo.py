#!/usr/bin/env python3
import errno
import os
import sys
from multiprocessing import Pool, cpu_count

from source.database_management.database import Database
from source.simulation_modules.simulation import Simulation


def write_file(path):
    folder = path.rsplit('/', 1)[0]
    try:
        os.makedirs(folder)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return open(path, 'w')


def simulate(chromosome):
    with write_file("output/" + chromosome.code + "_results.txt") as sys.stdout:
        print("[Simulation_Number]\t[Simulation_Duration]\t"
              "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
              "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t")

        # run simulations
        for i in range(int(sys.argv[2])):
            for replication_repair_duration in range(0, 8*3600, 8*3600):
                for transcription_start_delay in range(2000, 10, -2000):
                    for region in chromosome.transcription_regions:
                        setattr(region, 'delay', transcription_start_delay)
                    for origin in chromosome.replication_origins:
                        setattr(origin, 'replication_repair_duration', replication_repair_duration)

                    simulation = Simulation(chromosome)
                    simulation_duration, head_collisions, tail_collisions = simulation.run()
                    # print results
                    print("{}\t{}\t{}\t{}\t{}\t{}\t\n".format(i, simulation_duration, head_collisions, tail_collisions,
                                                              replication_repair_duration, transcription_start_delay))


def parse_arguments():
    with Database("db/simulation.sqlite") as db:
        if len(sys.argv) < 3:  # lacking arguments, therefore present available organisms
            print("Run with: ./KiReDyMo <organism> <number of simulations>")
            db.print_organisms()
            exit(1)
        else:
            return db.select_chromosomes(sys.argv[1])


def main():
    Pool(cpu_count()).map(simulate, parse_arguments())    # run each chromosome in a processor

if __name__ == "__main__":
    main()
