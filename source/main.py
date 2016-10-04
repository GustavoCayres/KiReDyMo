#!/usr/bin/env python3
# Run with python3 -m source.main 'Organism name' db/simulation_db.sqlite

import sys

from source.models.base_model import db
from source.models.chromosome import Chromosome
from source.simulation_modules.simulation import Simulation


def main(organism_name):

    db.connect()

    # chromosome setup
    chromosome = Chromosome.select().where(Chromosome.organism_name == organism_name)

    # output setup
    file_location = "output/" + organism_name.replace(' ', '-') + "_results.txt"
    sys.stdout = open(file_location, 'w')

    # simulation setup
    print(chromosome)
    print()
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
