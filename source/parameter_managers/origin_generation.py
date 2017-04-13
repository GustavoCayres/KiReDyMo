import math
from random import Random

from source.models.replication_origin import ReplicationOrigin

random_number_generator = Random()
random_number_generator.seed()


def generate_origins(chromosome, interorigin_distance):
    origin_amount = int(math.ceil(float(chromosome.length/interorigin_distance)))

    origins = []
    for i in range(origin_amount - len(chromosome.replication_origins)):
        position = random_number_generator.randrange(0, chromosome.length)
        while position in [origin.position for origin in chromosome.replication_origins]:
            position = random_number_generator.randrange(0, chromosome.length)
        origins.append(ReplicationOrigin(position, 0.1, chromosome.replication_speed, -1))

    return origins
