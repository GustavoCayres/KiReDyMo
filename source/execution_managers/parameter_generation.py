import copy
from random import Random

random_number_generator = Random()
random_number_generator.seed()


def generate_origins(chromosome):
    origins = sorted(chromosome.replication_origins).copy()
    return origins


def generate_simulation_parameters(chromosomes, number_of_simulations,
                                   replication_repair_duration, transcription_start_delay_range):
    parameters = []
    for chromosome in chromosomes:
        for i in range(number_of_simulations):
            origins = generate_origins(chromosome)
            for transcription_start_delay in range(*transcription_start_delay_range):
                chromosome_copy = copy.deepcopy(chromosome)
                chromosome_copy.replication_origins = origins
                chromosome_copy.replication_repair_duration = replication_repair_duration
                chromosome_copy.transcription_start_delay = transcription_start_delay
                parameters.append(chromosome_copy)
    return parameters
