from source.database_managers.database import Database


def parse_argument_file(file_path):
    code = None
    chromosomes = None
    number_of_simulations = None
    transcription_start_delay_range = None
    number_of_flexible_origins_range = None
    probability_of_origin_trigger_range = None
    replication_repair_duration = None
    is_transcription_active = None

    with open(file_path) as argument_file:
        for line in argument_file:
            line_list = line.split('\t')
            if line_list[0] == '[code]':
                code = line_list[1]
                chromosomes = []
                with Database('db/simulation.sqlite') as db:
                    for chromosome in db.select_chromosomes(code=code):
                        chromosomes.append(chromosome)

            elif line_list[0] == '[organism]':
                organism = line_list[1]
                chromosomes = []
                with Database('db/simulation.sqlite') as db:
                    for chromosome in db.select_chromosomes(organism=organism):
                        chromosomes.append(chromosome)

            elif line_list[0] == '[number_of_simulations]':
                number_of_simulations = int(line_list[1])

            elif line_list[0] == '[transcription_start_delay]':
                transcription_start_delay_range = [int(line_list[1]), int(line_list[2]), int(line_list[3])]

            elif line_list[0] == '[number_of_flexible_origins]':
                number_of_flexible_origins_range = [int(line_list[1]), int(line_list[2]), int(line_list[3])]

            elif line_list[0] == '[probability_of_origin_trigger]':
                probability_of_origin_trigger_range = [float(line_list[1]), float(line_list[2]), float(line_list[3])]

            elif line_list[0] == '[replication_repair_duration]':
                replication_repair_duration = int(line_list[1]) if line_list[1] != 'inf' else float('inf')

            elif line_list[0] == '[transcription_activity]':
                is_transcription_active = True if line_list[1] == "Yes" else False

        output_file_name = code

        return output_file_name, {'chromosomes': chromosomes,
                                  'number_of_simulations': number_of_simulations,
                                  'transcription_start_delay_range': transcription_start_delay_range,
                                  'number_of_flexible_origins_range': number_of_flexible_origins_range,
                                  'probability_of_origin_trigger_range': probability_of_origin_trigger_range,
                                  'replication_repair_duration': replication_repair_duration,
                                  'is_transcription_active': is_transcription_active
                                  }
