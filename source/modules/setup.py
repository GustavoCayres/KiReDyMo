from source.models.chromosome import Chromosome
from source.models.transcription_region import TranscriptionRegion
from source.simulation_modules.simulation import Simulation
import sys
from source.models.base_model import *


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


def simulate(chromosome):
    db.connect()

    # output setup
    file_location = "output/" + chromosome.code + "_results.txt"
    sys.stdout = open(file_location, 'w')

    # print simulated chromosome
    print(str(chromosome) + "\n")

    # run simulations
    for replication_repair_duration in range(0, 8*3600, 8*360):
        print("hey!")
        simulation = Simulation(chromosome, replication_repair_duration)
        simulation.run()
    db.close()
    sys.stdout.close()
