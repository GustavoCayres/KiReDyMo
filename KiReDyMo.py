#!/usr/bin/env python3
import errno
import os
import sys
from multiprocessing import Pool, cpu_count

from source.database_management.database import Database
from source.simulation_modules.simulation import Simulation

from source.simulation_management.simulation_parameters import *


def write_file(path):
    folder = path.rsplit('/', 1)[0]
    try:
        os.makedirs(folder)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return open(path, 'w')


def simulate(simulation_arguments):
    default_chromosome = simulation_arguments[0]
    number_of_simulations = simulation_arguments[1]
    with write_file("output/" + default_chromosome.code + "_results.txt") as sys.stdout:
        print("[Simulation_Number]\t[Simulation_Duration]\t"
              "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
              "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t")

        chromosome_list = chromosomes_with_update_attributes(default_chromosome)

        # run simulations
        for i in range(number_of_simulations):
            for chromosome in chromosome_list:
                simulation = Simulation(chromosome)
                simulation_duration, head_collisions, tail_collisions, repair_duration, transcription_delay =\
                    simulation.run()

                # print results
                print("{}\t{}\t{}\t{}\t{}\t{}\t\n".format(i+1, simulation_duration, head_collisions, tail_collisions,
                                                          repair_duration, transcription_delay))


def parse_arguments(args):
    with Database("db/simulation.sqlite") as db:
        if len(args) < 3:  # lacking arguments, therefore present available organisms
            print("Run with: ./KiReDyMo <organism> <number of simulations>")
            db.print_organisms()
            exit(1)
        else:
            parsed_args = []
            for chromosome in db.select_chromosomes(args[1]):
                parsed_args.append([chromosome, int(args[2])])
            return parsed_args


def main(args):
    Pool(cpu_count()).map(simulate, parse_arguments(args))    # run each chromosome in a processor

if __name__ == "__main__":
    main(sys.argv)
