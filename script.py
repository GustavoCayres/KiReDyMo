import os
import sys


output_path = "./output/"
chromosome_code = sys.argv[1]
with open(output_path + chromosome_code + "_results.txt", 'w') as chromosome_results_file:
    chromosome_results_file.write("Sim_Dur\tInter_Dist\tTrig_Orig\t\n")
    for simulation_folder_name in next(os.walk(output_path))[1]:
        line_list = []
        simulation_path = output_path + simulation_folder_name + "/"
        for result_file_name in next(os.walk(simulation_path))[2]:
            if result_file_name == (chromosome_code + ".txt"):
                file_path = simulation_path + result_file_name
                with open(file_path) as result_file:
                    result_file.readline()
                    for line in result_file:
                        line_list = line.split("\t")
                break
        chromosome_results_file.write(line_list[0]+"\t"+line_list[2]+"\t"+line_list[4]+"\t\n")
