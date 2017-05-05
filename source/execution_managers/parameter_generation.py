import copy
import math
from random import Random

from source.models.replication_origin import ReplicationOrigin

random_number_generator = Random()
random_number_generator.seed()


def generate_origins(chromosome, interorigin_distance):
    origin_amount = int(math.ceil(float(chromosome.length/interorigin_distance)))

    viable_positions = []
    for i in range(0, origin_amount):
        viable_positions.append(i * interorigin_distance)

    origins = []
    origins[:] = chromosome.replication_origins
    for i in range(origin_amount - len(chromosome.replication_origins)):
        position = random_number_generator.choice(viable_positions)
        while position in [origin.position for origin in origins]:
            position = random_number_generator.choice(viable_positions)
        origins.append(ReplicationOrigin(position, 0.1, chromosome.replication_speed, -1))

    return origins


def generate_simulation_parameters(chromosomes, number_of_unique_simulations, interorigin_distance,
                                   replication_repair_duration, transcription_start_delay_range):
    parameters = []
    for chromosome in chromosomes:
        for i in range(number_of_unique_simulations):
            origins = generate_origins(chromosome, interorigin_distance)
            for transcription_start_delay in range(*transcription_start_delay_range):
                chromosome_copy = copy.deepcopy(chromosome)
                chromosome_copy.replication_origins = origins
                chromosome_copy.replication_origins.sort()
                chromosome_copy.update_attributes(replication_repair_duration=replication_repair_duration)
                chromosome_copy.update_attributes(transcription_start_delay=transcription_start_delay)
                parameters.append(chromosome_copy)

    return parameters
