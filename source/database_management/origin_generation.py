import math
from random import Random


def generate_origins(chromosome, replication_speed, replication_repair_duration):
    d = chromosome.length
    v = replication_speed
    ts = 8 * 3600  # duration of S phase
    minimum_origin_amount = math.ceil(d / (2 * v * ts))

    origin_position = int(d / (1 + minimum_origin_amount))
    origins = []
    for i in range(minimum_origin_amount):
        origins.append(((i + 1) * origin_position, .1, replication_speed,
                        replication_repair_duration, chromosome.code, chromosome.organism))

    return origins


def generate_randomized_origins(chromosome, replication_speed, replication_repair_duration):
    d = chromosome.length
    v = replication_speed
    ts = 8 * 3600  # duration of S phase
    minimum_origin_amount = math.ceil(d / (2 * v * ts))

    random_number_generator = Random()
    random_number_generator.seed()

    origins = []
    for i in range(minimum_origin_amount):
        position = random_number_generator.randrange(0, chromosome.length)
        while position in [origin[0] for origin in origins]:
            position = random_number_generator.randrange(0, chromosome.length)
        origins.append((position, 1, replication_speed,
                        replication_repair_duration, chromosome.code, chromosome.organism))

    return origins


def generate_randomized_origins_in_inversions(chromosome, replication_speed, replication_repair_duration):
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

    origins = []
    for i in range(minimum_origin_amount):
        position = random_number_generator.choice(viable_positions)
        while position in [origin[0] for origin in origins]:
            position = random_number_generator.choice(viable_positions)
        origins.append((position, 1, replication_speed,
                        replication_repair_duration, chromosome.code, chromosome.organism))

    return origins
