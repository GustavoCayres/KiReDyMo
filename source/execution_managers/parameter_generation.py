import copy
from random import Random

from source.models.replication_origin import ReplicationOrigin

random_number_generator = Random()


def generate_origins(chromosome, bases_between_origins):
    number_of_flexible_origins = min(len(chromosome) - len(chromosome.constitutive_origins),
                                     int(len(chromosome) / bases_between_origins))
    score_of_flexible_origins = float(1/number_of_flexible_origins) if number_of_flexible_origins != 0 else None
    flexible_origins = []
    for i in range(number_of_flexible_origins):
        r = random_number_generator.randrange(len(chromosome))
        while r in [origin.position for origin in (chromosome.constitutive_origins + flexible_origins)]:
            r = random_number_generator.randrange(len(chromosome))

        flexible_origins.append(ReplicationOrigin(position=r, score=score_of_flexible_origins))

    return flexible_origins


def generate_simulation_parameters(chromosomes,
                                   transcription_start_delay,
                                   replication_repair_duration,
                                   is_transcription_active):

    parameters = []
    for chromosome in chromosomes:
        if replication_repair_duration is not None:
            chromosome.replication_repair_duration = replication_repair_duration
        if not is_transcription_active:
            chromosome.transcription_regions = []

        probability_of_origin_trigger = float(len(chromosome)/(260000 * 7080))

        chromosome.transcription_start_delay = transcription_start_delay

        parameters.append({'chromosome': copy.deepcopy(chromosome),
                           'probability_of_origin_trigger': probability_of_origin_trigger})

    return parameters
