#!/usr/bin/env python3
import sys
import time

from source.execution_managers.simulation_parallelization import run_parallel_simulations
from source.input_managers.file_parser import parse_argument_file
from source.output_managers.results_output import write_results


def main(args):
    start_time = time.time()

    parsed_arguments = parse_argument_file(file_path=args[1])

    results = run_parallel_simulations(parameter_generation_arguments=parsed_arguments)

    write_results(file_name=parsed_arguments['code'], results=results)

    print("Simulation Finished in %f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
