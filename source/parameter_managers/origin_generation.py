import math
from random import Random

from source.models.replication_origin import ReplicationOrigin

random_number_generator = Random()
random_number_generator.seed()


def generate_origins(chromosome, interorigin_distance):
    origin_amount = int(math.ceil(float(chromosome.length/interorigin_distance)))

    viable_positions = []
    for i in range(0, math.ceil(chromosome.length/interorigin_distance)):
        viable_positions.append(i * interorigin_distance)

    origins = []
    for i in range(origin_amount - len(chromosome.replication_origins)):
        position = random_number_generator.choice(viable_positions)
        while position in [origin.position for origin in chromosome.replication_origins]:
            position = random_number_generator.choice(viable_positions)
        origins.append(ReplicationOrigin(position, 0.1, chromosome.replication_speed, -1))

    return origins
