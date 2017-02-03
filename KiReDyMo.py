#!/usr/bin/env python3
import errno
import os
import sys
from multiprocessing import Pool, cpu_count

from source.database_management.database import Database
from source.simulation_modules.simulation import Simulation
from source.simulation_modules.simulation_parameters import ParameterIterator


def write_file(path):
    folder = path.rsplit('/', 1)[0]
    try:
        os.makedirs(folder)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return open(path, 'w')


def simulate(simulation_arguments):
    chromosome = simulation_arguments[0]
    number_of_simulations = simulation_arguments[1]

    parameters = ParameterIterator(chromosome, 8 * 3600, (0, 8 * 3600, 4 * 8 * 360), (2000, 10, 4 * -200))

    with write_file("output/" + chromosome.code + "_results.txt") as sys.stdout:
        print("[Simulation_Number]\t[Simulation_Duration]\t"
              "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
              "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t"
              "[Origins]\t")

        # run simulations
        for i in range(number_of_simulations):
            for parameter in parameters:
                simulation = Simulation(parameter)

                simulation_duration, head_collisions, tail_collisions, repair_duration, transcription_delay, origins =\
                    simulation.run()
                parameters.last_simulation_duration = simulation_duration

                # print results
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t\n".format(i+1, simulation_duration,
                                                              head_collisions, tail_collisions,
                                                              repair_duration, transcription_delay,
                                                              [str(origin) for origin in origins]))


def parse_arguments(args):
    with Database("db/simulation.sqlite") as db:
        if len(args) < 2:  # lacking arguments, therefore alert
            print("Run with: ./KiReDyMo <file_with_parameters>")
            exit(1)
        else:
            with open(args[1]) as parameter_file:
                organism_name = parameter_file.readline().strip('\n')
                number_of_simulations = int(parameter_file.readline())
            parsed_arguments = []
            for chromosome in db.select_chromosomes(organism=organism_name):
                parsed_arguments.append([chromosome, number_of_simulations])
            return parsed_arguments


def main(args):
    Pool(cpu_count()).map(simulate, parse_arguments(args))    # run each chromosome in a processor

if __name__ == "__main__":
    main(sys.argv)
