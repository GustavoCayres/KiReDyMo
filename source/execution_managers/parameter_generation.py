import copy
from random import Random

from source.models.replication_origin import ReplicationOrigin

random_number_generator = Random()


def generate_origins(chromosome, number_of_origins, score_of_new_origins):
    number_of_origins = min((len(chromosome), number_of_origins))

    origins = chromosome.replication_origins.copy()
    for i in range(number_of_origins - len(chromosome.replication_origins)):
        r = random_number_generator.randrange(len(chromosome))
        while r in [origin.position for origin in origins]:
            r = random_number_generator.randrange(len(chromosome))

        origins.append(ReplicationOrigin(position=r, score=score_of_new_origins))

    return sorted(origins)


def generate_simulation_parameters(chromosomes, number_of_simulations,
                                   replication_repair_duration, transcription_start_delay_range):
    parameters = []
    for chromosome in chromosomes:
        for i in range(number_of_simulations):
            origins = generate_origins(chromosome=chromosome, number_of_origins=300, score_of_new_origins=.5)
            for transcription_start_delay in range(*transcription_start_delay_range):
                chromosome_copy = copy.deepcopy(chromosome)
                chromosome_copy.replication_origins = origins
                chromosome_copy.replication_repair_duration = replication_repair_duration
                chromosome_copy.transcription_start_delay = transcription_start_delay
                parameters.append(chromosome_copy)

    return parameters
