#!/usr/bin/env python3
import errno
import os
import sys
from multiprocessing import Pool, cpu_count

from source.database_management.database import Database
from source.parameter_managers.origin_generation import *
from source.simulation_modules.simulation import Simulation


def open_output(file_name):
    path = "output/" + file_name
    output_file = open(path, 'a')
    if os.path.getsize(path) == 0:
        print("[Simulation_Duration]\t"
              "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
              "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t"
              "[Origins]\t", file=output_file)
    return output_file


def simulate(chromosome):
    with open_output(chromosome.code + "_results.txt") as output_file:
        for i in range(int(sys.argv[2])):
            chromosome.replication_origins = generate_randomized_origins(chromosome, 67, 0)
            for repair_duration in range(0, 28800, 11520):
                for transcription_delay in range(10, 2000, 200):
                    chromosome.update_attributes(transcription_start_delay=transcription_delay,
                                                 replication_repair_duration=repair_duration)

                    simulation = Simulation(chromosome)
                    simulation_duration, head_collisions, tail_collisions, repair_duration,\
                        transcription_delay, origins = simulation.run()

                    result = "{}\t{}\t{}\t{}\t{}\t{}\t".format(simulation_duration,
                                                               head_collisions, tail_collisions,
                                                               repair_duration, transcription_delay,
                                                               [str(origin) for origin in origins])

                    print(result, file=output_file)
                    output_file.flush()


def parse_arguments(file_name):
    with Database("db/simulation.sqlite") as db:
        with open(file_name) as parameter_file:
            organism_name = parameter_file.readline().strip('\n')

            parsed_arguments = []
            for chromosome in db.select_chromosomes(code="TcChr1-S") + db.select_chromosomes(code="TcChr2-S"): #organism=organism_name):
                parsed_arguments.append(chromosome)
            return parsed_arguments


def main():
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    Pool(cpu_count()).map(simulate, parse_arguments(sys.argv[1]))    # run each chromosome in a processor

if __name__ == "__main__":
    if len(sys.argv) < 2:  # lacking arguments, therefore alert
        print("Run with: ./KiReDyMo <file_with_parameters>")
        exit(1)
    main()
