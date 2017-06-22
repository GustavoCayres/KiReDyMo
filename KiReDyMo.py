#!/usr/bin/env python3
import sys
import time

from source.execution_managers.file_parser import parse_argument_file
from source.execution_managers.simulation_parallelization import run_parallel_simulations
from source.output_managers.results_output import write_overall_results, write_origin_trigger_log


def main(args):
    start_time = time.time()

    parsed_arguments = parse_argument_file(file_path=args[1])

    results = run_parallel_simulations(parameter_generation_arguments=parsed_arguments)

    file_names = [result[0] for result in results]
    overall_results = [result[0:-1] for result in results]
    write_overall_results(file_names=file_names, results=overall_results)

    print("Simulation Finished in %f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
