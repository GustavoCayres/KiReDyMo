import copy
from random import Random

from source.models.replication_origin import ReplicationOrigin

random_number_generator = Random()
random_number_generator.seed()


def generate_origins(chromosome, interorigin_distance):
    origins = []
    origins[:] = sorted(chromosome.replication_origins)
    i = 0
    while i < len(origins):
        origin_position = origins[i].position
        if i + 1 >= len(origins):
            if (chromosome.length - 1) - origin_position >= interorigin_distance:
                origins.insert(i + 1, ReplicationOrigin(origin_position + interorigin_distance, 0.1,
                                                        chromosome.replication_speed, -1))
        else:
            if origins[i + 1].position - origin_position >= 2 * interorigin_distance:
                origins.insert(i + 1, ReplicationOrigin(origin_position + interorigin_distance, 0.1,
                                                        chromosome.replication_speed, -1))

        i += 1

    return origins


def generate_simulation_parameters(chromosomes, number_of_simulations, interorigin_distance,
                                   replication_repair_duration, transcription_start_delay_range):
    parameters = []
    for chromosome in chromosomes:
        for i in range(number_of_simulations):
            origins = generate_origins(chromosome, interorigin_distance)
            for transcription_start_delay in range(*transcription_start_delay_range):
                chromosome_copy = copy.deepcopy(chromosome)
                chromosome_copy.replication_origins = origins
                chromosome_copy.replication_origins.sort()
                chromosome_copy.update_attributes(replication_repair_duration=replication_repair_duration)
                chromosome_copy.update_attributes(transcription_start_delay=transcription_start_delay)
                parameters.append(chromosome_copy)

    return parameters
