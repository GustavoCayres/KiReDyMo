import math

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
