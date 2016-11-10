#!/usr/bin/env python3
# Run with python3 -m source.main 'Organism name'

import random
import sys

from source.models.chromosome import Chromosome
from source.modules.setup import arguments, simulate, create_folder
from multiprocessing import Pool, cpu_count


def main(organism_name):
    random.seed()

    p = Pool(cpu_count())          # create a thread for each processor
    p.map(simulate, [chromosome for chromosome
                     in Chromosome.select().where(Chromosome.organism == organism_name and Chromosome.code == "TcChr1-S")])


if __name__ == "__main__":
    main(arguments(sys.argv))
