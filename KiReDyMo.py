#!/usr/bin/env python3
import errno
import os
import sys
from multiprocessing import Pool, cpu_count

from source.database_management.database import Database
from source.simulation_modules.simulation import Simulation
from source.simulation_modules.parameter_iterator import ParameterIterator


def open_output(file_name):
    path = "output/" + file_name
    output_file = open(path, 'a')
    if os.path.getsize(path) == 0:
        print("[Simulation_Duration]\t"
              "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
              "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t"
              "[Origins]\t", file=output_file)
    return output_file


def simulate(simulation_arguments):
    chromosome = simulation_arguments[0]
    repair_duration_range = simulation_arguments[1]
    transcription_delay_range = simulation_arguments[2]

    parameters = ParameterIterator(chromosome, 8 * 3600, repair_duration_range, transcription_delay_range)

    with open_output(chromosome.code + "_results.txt") as output_file:
        for parameter in parameters:
            simulation = Simulation(parameter)

            simulation_duration, head_collisions, tail_collisions, repair_duration, transcription_delay, origins =\
                simulation.run()
            parameters.last_simulation_duration = simulation_duration

            # print results
            print("{}\t{}\t{}\t{}\t{}\t{}\t\n".format(simulation_duration,
                                                      head_collisions, tail_collisions,
                                                      repair_duration, transcription_delay,
                                                      [str(origin) for origin in origins]), file=output_file)


def parse_arguments(file_name):
    with Database("db/simulation.sqlite") as db:
        with open(file_name) as parameter_file:
            organism_name = parameter_file.readline().strip('\n')
            repair_duration_range = [int(x) for x in parameter_file.readline().split()]
            transcription_delay_range = [int(x) for x in parameter_file.readline().split()]

            parsed_arguments = []
            for chromosome in db.select_chromosomes(code="TcChr2-S"): # organism=organism_name):
                parsed_arguments.append([chromosome, repair_duration_range, transcription_delay_range])
            return parsed_arguments


def seed():
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


def main(args):
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    for i in range(int(args[2])):
        seed()
        Pool(cpu_count()).map(simulate, parse_arguments(args[1]))    # run each chromosome in a processor

if __name__ == "__main__":
    if len(sys.argv) < 2:  # lacking arguments, therefore alert
        print("Run with: ./KiReDyMo <file_with_parameters>")
        exit(1)
    main(sys.argv)
