import sys
import os

N_set = set()
O_set = set()

results_path = sys.argv[1]
for simulation_folder_name in next(os.walk(results_path))[1]:
    simulation_path = results_path + simulation_folder_name + "/"
    for result_file_name in next(os.walk(simulation_path))[2]:
        result_path = simulation_path + result_file_name
        with open(result_path) as result_file:
            result_file.readline()
            split_line = result_file.readline().split('\t')
            N_set.add(split_line[3])
            O_set.add(split_line[5])

chart_dict = dict()
for i in N_set:
    for j in O_set:
        chart_dict[(i, j)] = [0, 0, 0]

for simulation_folder_name in next(os.walk(results_path))[1]:
    simulation_path = results_path + simulation_folder_name + "/"
    time = 0
    for result_file_name in next(os.walk(simulation_path))[2]:
        result_path = simulation_path + result_file_name
        with open(result_path) as result_file:
            result_file.readline()
            split_line = result_file.readline().split('\t')
            chart_dict[(split_line[3], split_line[5])][1] += round(float(split_line[2]))
            chart_dict[(split_line[3], split_line[5])][2] += 1
            time = max(float(split_line[0]), time)
        chart_dict[(split_line[3], split_line[5])][0] += time * chart_dict[(split_line[3], split_line[5])][2]

with open("chart.txt", 'w') as output_file:
    output_file.write("N\tO\ttime\tinter\t\n")
    for key, value in chart_dict.items():
        line = "{}\t{}\t{}\t{}\t\n".format(key[0], key[1], value[0]/value[2], value[1]/value[2])
        output_file.write(line)
