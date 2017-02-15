import math
from random import Random

from source.models.replication_origin import ReplicationOrigin


def generate_origins(chromosome, replication_speed, replication_repair_duration):
    d = chromosome.length
    v = replication_speed
    ts = 8 * 3600  # duration of S phase
    minimum_origin_amount = math.ceil(d / (2 * v * ts))

    origin_position = int(d / (1 + minimum_origin_amount))
    origins = []
    for i in range(minimum_origin_amount):
        origins.append(ReplicationOrigin((i + 1) * origin_position, 1, replication_speed, replication_repair_duration))

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
        origins.append(ReplicationOrigin(position, 1, replication_speed, replication_repair_duration))

    return origins
