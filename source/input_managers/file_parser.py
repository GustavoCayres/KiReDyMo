from source.database_managers.database import Database


def parse_argument_file(file_path):
    code = ""
    chromosomes = []
    number_of_simulations = -1
    replication_repair_duration = -1
    transcription_start_delay_range = -1
    interorigin_distance = -1

    with open(file_path) as argument_file:
        for line in argument_file:
            line_list = line.split('\t')
            if line_list[0] == '[code]':
                code = line_list[1]
                with Database('db/simulation.sqlite') as db:
                    for chromosome in db.select_chromosomes(code=code):
                        chromosomes.append(chromosome)
            elif line_list[0] == '[number_of_simulations]':
                number_of_simulations = int(line_list[1])
            elif line_list[0] == '[replication_repair_duration]':
                if line_list[1] == 'inf':
                    replication_repair_duration = float('inf')
                else:
                    replication_repair_duration = int(line_list[1])
            elif line_list[0] == '[transcription_start_delay]':
                transcription_start_delay_range = [int(line_list[1]), int(line_list[2]), int(line_list[3])]
            elif line_list[0] == '[interorigin_distance]':
                interorigin_distance = int(line_list[1])

        return {'code': code,
                'chromosomes': chromosomes,
                'number_of_simulations': number_of_simulations,
                'replication_repair_duration': replication_repair_duration,
                'transcription_start_delay_range': transcription_start_delay_range,
                'interorigin_distance': interorigin_distance}
