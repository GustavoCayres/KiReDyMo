#!/usr/bin/env python3
# Run with python3 -m source.main 'Trypanosoma test' db/simulation_db.sqlite

from .simulation import Simulation
from db.database_import import DatabaseImport
import sys


def main(organism_name, database_path):
    # chromosome setup
    db = DatabaseImport(database_path)
    chromosome = db.import_chromosome_by_organism(organism_name)

    # output setup
    file_location = "output/" + organism_name.replace(' ', '-') + "_results.txt"
    sys.stdout = open(file_location, 'w')

    # simulation setup
    print(chromosome + "\n")
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
    main(sys.argv[1], sys.argv[2])
