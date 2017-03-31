#!/usr/bin/env python3
import sys


for i in range(int(sys.argv[1])):
    index = str(i+1).zfill(2)
    file_name = "origin_Tb927_" + index + "_v5.1.txt"
    with open(file_name, 'w') as f:
        print("[Code]\t[Position]\t[Score]\t", file=f)
        print("Tb927_" + index + "_v5.1\t", file=f)
