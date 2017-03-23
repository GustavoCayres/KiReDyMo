#!/usr/bin/env python3
import sys


for i in range(int(sys.argv[1])):
    index = str(i+1)
    file_name = "origin_" + index + ".txt"
    with open(file_name, 'w') as f:
        print("[Code]\t[Organism]\t", file=f)
        print("Tb927_" + index + "_v5.1\tTrypanosoma brucei brucei TREU927\t", file=f)
