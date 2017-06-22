import errno
import os


def write_overall_results(file_names, results):
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    for file_name in file_names:
        with open("output/" + file_name + ".txt", 'w') as results_file:
            results_file.write("[Sim_Dur]\t"
                               "[#_Head_Col]\t"
                               "[Interorig_Dist]\t"
                               "[Transcript_Start_Delay]\t"
                               "[#_Orig_Trig]\t"
                               "[#_Orig_Gen]\t"
                               "[Duplic_%]\t"
                               "\n")

            for result in results:
                if result[0] == file_name:
                    result_line = ""
                    for data in result[1:]:
                        result_line += "{}\t".format(data)
                    result_line += "\n"
                    results_file.write(result_line)


def write_origin_trigger_log(file_name, results):
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    with open("output/" + file_name + ".txt", 'w') as results_file:
        results_file.write("[Simulation_Time]\t"
                           "[Triggered Origin]\t"
                           "\n")
        for result in results:
            for time, origin in result.items():
                result_line = "{}\t{}\t".format(time, origin)
                result_line += "\n"
                results_file.write(result_line)
