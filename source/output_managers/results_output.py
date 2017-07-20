import errno
import os


def make_output_directory(simulation_number):
    directory_path = "output/"

    try:
        os.makedirs(directory_path)

    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    directory_path += "simulation_" + str(simulation_number) + "/"
    try:
        os.makedirs(directory_path)

    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    return directory_path


def write_overall_results(folder_path, results):
    for result in results:
        with open(folder_path + result[0] + ".txt", 'w') as output_file:
            output_file.write("[Sim_Dur]\t"
                              "[#_Head_Col]\t"
                              "[Interorig_Dist]\t"
                              "[Transcript_Start_Delay]\t"
                              "[#_Orig_Trig]\t"
                              "[#_Orig_Gen]\t"
                              "[Duplic_%]\t"
                              "\n")
            result_line = ""
            for data in result[1:-1]:
                result_line += "{}\t".format(data)

            result_line += "\n"
            output_file.write(result_line)


def write_origin_trigger_log(file_names, results):
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    for file_name in file_names:
        with open("output/log_" + file_name + ".txt", 'w') as results_file:
            results_file.write("[Simulation_Time]\t"
                               "[Triggered Origin]\t"
                               "\n")
            for result in results:
                if result[0] == file_name:
                    for time, origin in result[1].items():
                        result_line = "{}\t{}\t".format(time, origin)
                        result_line += "\n"
                        results_file.write(result_line)
