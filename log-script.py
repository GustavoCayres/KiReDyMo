import os


output_path = "./output/"
joined_logs_path = "./joined_logs/"
for simulation_folder_name in next(os.walk(output_path))[1]:
    simulation_path = output_path + simulation_folder_name + "/"
    os.makedirs(joined_logs_path, exist_ok=True)
    os.makedirs(joined_logs_path + "valid/", exist_ok=True)
    os.makedirs(joined_logs_path + "not_valid/", exist_ok=True)
    valid = True
    for result_file_name in next(os.walk(simulation_path))[2]:
        result_path = simulation_path + result_file_name
        with open(result_path) as result_file:
            result_file.readline()
            split_line = result_file.readline().split('\t')
            if int(split_line[0]) > 7080 or abs(float(split_line[2]) - 260000) > 260000*.1:
                valid = False

    final_path = joined_logs_path + "valid/" if valid else joined_logs_path + "not_valid/"
    with open(final_path + "valid.txt", 'a') as joined_logs_file:
        for log_folder in next(os.walk(simulation_path))[1]:
            log_path = simulation_path + log_folder + "/"
            eteds = []
            for log_file_name in next(os.walk(log_path))[2]:
                file_path = log_path + log_file_name
                with open(file_path) as log_file:
                    origins = []
                    log_file.readline()
                    for line in log_file:
                        origins.append(int(line.split('\t')[1]))

                    origins.sort()
                    eted_start = 0
                    for origin in origins:
                        eteds.append(str(origin - eted_start) + '\n')
                        eted_start = origin

            joined_logs_file.writelines(eteds)
