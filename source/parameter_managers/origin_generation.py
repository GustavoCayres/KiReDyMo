import math
from random import Random

from source.models.replication_origin import ReplicationOrigin


def generate_origins(chromosome, replication_speed, replication_repair_duration):  # TODO
    d = chromosome.length
    v = replication_speed
    ts = 8 * 3600  # duration of S phase
    minimum_origin_amount = math.ceil(d / (2 * v * ts))

    origin_position = int(d / (1 + minimum_origin_amount))
    origins = []
    for i in range(minimum_origin_amount):
        origins.append(ReplicationOrigin((i + 1) * origin_position, 1, replication_speed, replication_repair_duration))

    return origins


def generate_randomized_origins(chromosome, number_of_sets, replication_speed, replication_repair_duration):
    d = chromosome.length
    v = replication_speed
    ts = 8 * 3600  # duration of S phase
    minimum_origin_amount = math.ceil(d / (2 * v * ts))

    random_number_generator = Random()
    random_number_generator.seed()

    list_of_origins_sets = []
    for i in range(number_of_sets):
        origins_set = []
        for j in range(minimum_origin_amount):
            position = random_number_generator.randrange(0, chromosome.length)
            while position in [origin.position for origin in origins_set]:
                position = random_number_generator.randrange(0, chromosome.length)
            origins_set.append(ReplicationOrigin(position, 1, replication_speed, replication_repair_duration))
        list_of_origins_sets.append(origins_set)

    return list_of_origins_sets


def generate_randomized_origins_in_inversions(chromosome, number_of_sets,
                                              replication_speed, replication_repair_duration):
    d = chromosome.length
    v = replication_speed
    ts = 8 * 3600  # duration of S phase
    minimum_origin_amount = math.ceil(d / (2 * v * ts))

    random_number_generator = Random()
    random_number_generator.seed()

    viable_positions = []
    for transcription_region in chromosome.transcription_regions:
        viable_positions.append(transcription_region.start)
        viable_positions.append(transcription_region.end)

    list_of_origins_sets = []
    for i in range(number_of_sets):
        origins_set = []
        for j in range(minimum_origin_amount):
            position = random_number_generator.choice(viable_positions)
            while position in [origin.position for origin in origins_set]:
                position = random_number_generator.choice(viable_positions)
            origins_set.append(ReplicationOrigin(position, 1, replication_speed, replication_repair_duration))
        list_of_origins_sets.append(origins_set)

    return list_of_origins_sets
