import errno
import os


def write_results(file_name, results):
    try:
        os.makedirs("output")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    with open("output/" + file_name, 'w') as results_file:
        results_file.write("[Simulation_Duration]\t"
                           "[Head_Collision_Amount]\t"
                           "[Tail_Collision_Amount]\t"
                           "[Interorigin_Distance]\t"
                           "[Transcription_Start_Delay]\t"
                           "[Origins]\t"
                           "[Final_Chromosome_State]\t"
                           "\n")

        for result in results:
            result_line = ""
            for data in result:
                result_line += "{}\t".format(data)
            result_line += "\n"
            results_file.write(result_line)
