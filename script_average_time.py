import sys
import os

results_path = sys.argv[1]
for simulation_folder_name in next(os.walk(results_path))[1]:
    simulation_path = results_path + simulation_folder_name + "/"
    for result_file_name in next(os.walk(simulation_path))[2]:
        result_path = simulation_path + result_file_name
        with open(result_path) as result_file:
            result_file.readline()
            split_line = result_file.readline().split('\t')
            if split_line[3] == "15":
                with open(result_file_name, 'a') as output_file:
                    output_file.write(split_line[0] + "\n")
