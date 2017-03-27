import re
import os


def aggregate_output():
    for file_name in os.listdir("output"):
        regex = re.match("(.+)_[0-9]+_results", file_name)
        if regex is not None:
            output_path = "output/" + regex.group(1) + "_results.txt"
            with open(output_path, 'a') as output_file:
                if os.path.getsize(output_path) == 0:
                    print("[Simulation_Duration]\t"
                          "[Head_Collision_Amount]\t[Tail_Collision_Amount]\t"
                          "[Replication_Repair_Duration]\t[Transcription_Start_Delay]\t"
                          "[Origins]\t", file=output_file)

                file_path = "output/" + file_name
                with open(file_path, 'r') as partial_file:
                    output_file.write(partial_file.read())

            os.remove(file_path)

if __name__ == "__main__":
    aggregate_output()
