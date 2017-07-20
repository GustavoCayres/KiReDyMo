#!/usr/bin/env python3
import sys
import time

from source.execution_managers.file_parser import parse_argument_file
from source.execution_managers.simulation_parallelization import run_parallel_simulations


def main(args):
    start_time = time.time()
    print("Started parsing...")
    parsed_arguments = parse_argument_file(file_path=args[1])
    print("Parsing complete.")
    print("Started simulation...")
    run_parallel_simulations(**parsed_arguments)
    print("Simulation complete.")
    print("Program finished in %f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
