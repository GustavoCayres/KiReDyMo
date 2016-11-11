from source.models.chromosome import Chromosome
from source.models.transcription_region import TranscriptionRegion
from source.simulation_modules.simulation import Simulation
import sys
import os
import errno
from source.models.base_model import *


def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def arguments(argument_list):
    if len(argument_list) == 1:
        print("Organisms currently in the database are:")
        possible_organisms = dict()
        for index, chromosome in enumerate(Chromosome.select(Chromosome.organism).distinct()):
            print(str(index) + "\t" + str(chromosome.organism))
            possible_organisms[index] = chromosome.organism
        print()
        return possible_organisms[int(input("Specify an organism (by index): "))]
    elif len(argument_list) == 2:
        return argument_list[1]
    else:
        print("Too many arguments.")
        exit(1)


def print_simulation_results(*args):
    for data in args:
        print(data, end='\t')
    print()


def simulate(chromosome):
    db.connect()

    # output setup
    file_location = "output/" + chromosome.code + "_results.txt"
    sys.stdout = open(file_location, 'w')

    # print simulated chromosome
    print("[Simulation_Number]\t[Simulation_Duration]\t"
          "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
          "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t")

    # run simulations
    i = 0
    for replication_repair_duration in range(0, 8*3600, 8*360):
        for transcription_start_delay in range(10, 2000, 200):
            simulation = Simulation(chromosome, replication_repair_duration, transcription_start_delay)
            simulation_duration, head_collisions, tail_collisions = simulation.run()
            i += 1
            print_simulation_results(i, simulation_duration, head_collisions, tail_collisions,
                                     replication_repair_duration, transcription_start_delay)

    db.close()
    sys.stdout.close()
