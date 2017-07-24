import errno
import os
import shutil


def make_simulation_directory(simulation_number):
    directory_path = "output/simulation_" + str(simulation_number) + "/"
    os.makedirs(directory_path)
    return directory_path


def make_output_directory():
    while True:
        try:
            os.makedirs("output/")

        except OSError as exception:
            if exception.errno == errno.EEXIST:
                shutil.rmtree("output/")

            else:
                raise

            continue

        break


def write_overall_results(folder_path, results):
    chromosome_code_set = set()
    for result in results:
        chromosome_code_set.add(result[0])

    for chromosome_code in chromosome_code_set:
        os.makedirs(folder_path + chromosome_code + "_log/")

        with open(folder_path + chromosome_code + ".txt", 'w') as output_file:
            output_file.write("[Sim_Dur]\t"
                              "[#_Head_Col]\t"
                              "[Interorig_Dist]\t"
                              "[Transcript_Start_Delay]\t"
                              "[#_Orig_Trig]\t"
                              "[#_Orig_Gen]\t"
                              "[Duplic_%]\t"
                              "[Log]\t"
                              "\n")

            i = 0
            for result in results:
                if result[0] == chromosome_code:
                    i += 1
                    write_origin_trigger_log(log_file_path=folder_path + chromosome_code + "_log/" + str(i) + ".txt",
                                             log=result[-1])
                    result[-1] = i
                    result_line = ""
                    for data in result[1:]:
                        result_line += "{}\t".format(data)

                    result_line += "\n"
                    output_file.write(result_line)


def write_origin_trigger_log(log_file_path, log):
        with open(log_file_path, 'w') as results_file:
            results_file.write("[Simulation_Time]\t"
                               "[Triggered Origin]\t"
                               "\n")
            for time, origin in log.items():
                result_line = "{}\t{}\t".format(time, origin)
                result_line += "\n"
                results_file.write(result_line)
