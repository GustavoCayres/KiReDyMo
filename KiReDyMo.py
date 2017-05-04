#!/usr/bin/env python3
import errno
import os
import sys
import time

from source.input_managers.file_parser import parse_argument_file
from source.execution_managers.simulation_parallelization import run_parallel_simulations
from source.output_managers.aggregate_output import aggregate_output


def main(args):
    start_time = time.time()

    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    parsed_arguments = parse_argument_file(file_path=args[1])

    run_parallel_simulations(parameter_generation_arguments=parsed_arguments)

    aggregate_output()
    print("Simulation Finished in %f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
