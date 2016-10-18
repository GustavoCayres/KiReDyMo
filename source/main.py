#!/usr/bin/env python3
# Run with python3 -m source.main 'Organism name'

import sys

from source.models.chromosome import Chromosome
from source.simulation_modules.simulation import Simulation
from source.models.transcription_region import TranscriptionRegion


def main(organism_name):

    # chromosome setup
    chromosome = Chromosome.get(Chromosome.organism == organism_name)

    # output setup
    file_location = "output/" + organism_name.replace(' ', '-') + "_results.txt"
    sys.stdout = open(file_location, 'w')

    # print simulated chromosome
    print(chromosome + "\n")

    # setup simulation
    simulation = Simulation(chromosome)
    simulation.begin()
    steps = 0
    while simulation.replication.left_fork is not None or simulation.replication.right_fork is not None:
        simulation.step()
        steps += 1
        print(simulation.replication.left_fork, simulation.replication.right_fork)
        print("--------------------------------------------")
    print("Total steps: ", steps)

    sys.stdout.close()

if __name__ == "__main__":
    main(sys.argv[1])
