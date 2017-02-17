#!/usr/bin/env python3
import copy
import errno
import os
import sys
from multiprocessing import Pool

from source.database_management.database import Database
from source.parameter_managers.origin_generation import *
from source.simulation_modules.simulation import Simulation


def simulate(args):
    chromosome = args[0]
    simulation_number = args[1]

    with open("output/" + chromosome.code + "_" + str(simulation_number) + "_results.txt", 'w') as output_file:
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
            for chromosome in db.select_chromosomes(code="TcChr1-S"):    # organism=organism_name):
                parsed_arguments.append(chromosome)
            return parsed_arguments


def main(args):
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    cores = Pool()
    chromosomes = []
    for chromosome in parse_arguments(args[1]):
        simulation_counter = 1
        for replication_origins in generate_randomized_origins(chromosome, int(args[2]), 67, 0):
            for replication_repair_duration in range(0, 28800, 11520):
                for transcription_start_delay in range(10, 2000, 700):
                    chromosome_copy = copy.deepcopy(chromosome)
                    chromosome_copy.update_attributes(transcription_start_delay=transcription_start_delay,
                                                      replication_repair_duration=replication_repair_duration,
                                                      replication_origins=replication_origins)
                    chromosomes.append((chromosome_copy, simulation_counter))
                    simulation_counter += 1
    cores.map(simulate, chromosomes)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
