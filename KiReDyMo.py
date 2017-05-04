#!/usr/bin/env python3
import copy
import errno
import os
import sys
import time
import math
from multiprocessing import Pool

from source.database_managers.database import Database
from source.output_managers.aggregate_output import aggregate_output
from source.simulation_modules.simulation import Simulation
from source.parameter_managers.origin_generation import generate_origins


def simulate(args):
    chromosome = args[0]
    simulation_number = args[1]

    simulation = Simulation(chromosome)
    simulation_duration, head_collisions, tail_collisions, repair_duration,\
        transcription_delay, origins = simulation.run()
    result = "{}\t{}\t{}\t{}\t{}\t{}\t\n".format(simulation_duration,
                                                 head_collisions, tail_collisions,
                                                 repair_duration, transcription_delay,
                                                 [str(origin) for origin in origins])

    with open("output/" + chromosome.code + "_" + str(simulation_number) + "_results.txt", 'w') as output_file:
        output_file.write(result)


def parse_arguments(file_name):
    with open(file_name) as parameter_file:
        query = parameter_file.readline().strip("\n").split('\t')
        with Database("db/simulation.sqlite") as db:
            chromosomes = []
            for chromosome in db.select_chromosomes(**{query[0]: query[1]}):
                chromosomes.append(chromosome)
        random_origins_amount = int(parameter_file.readline())
        replication_repair_duration_range = [int(i) for i in parameter_file.readline().strip("\n").split('\t')]
        transcription_start_delay_range = [int(i) for i in parameter_file.readline().strip("\n").split('\t')]

        return chromosomes, random_origins_amount, replication_repair_duration_range, transcription_start_delay_range


def simulation_parameters(chromosomes, number_of_unique_simulations,
                          replication_repair_duration_range, transcription_start_delay_range):
    parameters = []
    for chromosome in chromosomes:
        simulation_counter = 1
        for i in range(number_of_unique_simulations):
            origins = generate_origins(chromosome, 260000)
            replication_repair_duration = 0
            for transcription_start_delay in range(*transcription_start_delay_range):
                chromosome_copy = copy.deepcopy(chromosome)
                chromosome_copy.replication_origins.extend(origins)
                chromosome_copy.update_attributes(replication_repair_duration=replication_repair_duration)
                chromosome_copy.update_attributes(transcription_start_delay=transcription_start_delay)
                parameters.append((chromosome_copy, simulation_counter))
                simulation_counter += 1

    return parameters


def main(args):
    start_time = time.time()

    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    cores = Pool()

    cores.map(simulate, simulation_parameters(*parse_arguments(args[1])))
    aggregate_output()
    print("Simulation Finished in %f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
