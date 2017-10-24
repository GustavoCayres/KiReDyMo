#!/usr/bin/env python3

#
# KiReDyMo.py: main program of the KiReDyMo program.
#
#    This file is part of the KiReDyMo program.
#
#    Copyright (C) 2017 Gustavo Rodrigues Cayres-Silva and Marcelo S. Reis.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import sys
import time

from source.execution_managers.file_parser import parse_argument_file
from source.execution_managers.simulation_parallelization import run_parallel_simulations


def main(args):
    start_time = time.time()
    parsed_arguments = parse_argument_file(file_path=args[1])
    print("Parsing complete.")
    print("Started simulations...")
    run_parallel_simulations(**parsed_arguments)
    print("Program finished in %f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run with: ./KiReDyMo <file_with_parameters>", file=sys.stderr)
        exit(1)
    main(sys.argv)
