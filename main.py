#!/usr/bin/env python3
# Run with python3 -m source.main 'Organism name'

import random
import sys

from source.models.chromosome import Chromosome
# noinspection PyUnresolvedReferences
from source.models.transcription_region import TranscriptionRegion
from source.simulation_modules.simulation import Simulation


def help_if_no_arguments():
    if len(sys.argv) == 1:
        print("Organisms currently in the database are:")
        possible_organisms = dict()
        for index, chromosome in enumerate(Chromosome.select(Chromosome.organism).distinct()):
            print(str(index) + "\t" + str(chromosome.organism))
            possible_organisms[index] = chromosome.organism
        print()
        sys.argv.append(possible_organisms[int(input("Specify an organism (by index): "))])


def main(organism_name):
    random.seed()

    for chromosome in Chromosome.select().where(Chromosome.organism == organism_name).order_by(Chromosome.code):
        print("Simulating chromosome " + str(chromosome.code), file=sys.stderr)

        # output setup
        file_location = "output/" + chromosome.code + "_results.txt"
        sys.stdout = open(file_location, 'w')

        # print simulated chromosome
        print(str(chromosome) + "\n")

        # run simulation
        simulation = Simulation(chromosome)
        simulation.run()

    sys.stdout.close()


if __name__ == "__main__":
    help_if_no_arguments()
    main(sys.argv[1])
