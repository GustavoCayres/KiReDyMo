#!/usr/bin/env python3
# Run with python3 -m source.main 'Organism name'

import sys

from source.models.chromosome import Chromosome
from source.simulation_modules.simulation import Simulation
from source.models.transcription_region import TranscriptionRegion
import random


def main(organism_name):

    # output setup
    file_location = "output/" + organism_name.replace(' ', '-') + "_results.txt"
    sys.stdout = open(file_location, 'w')

    random.seed()

    for chromosome in Chromosome.select().where(Chromosome.organism == organism_name):
        # run simulation
        Simulation.start(chromosome)

    print("Total Duration: " + str(Simulation.total_duration))
    sys.stdout.close()

if __name__ == "__main__":
    main(sys.argv[1])
