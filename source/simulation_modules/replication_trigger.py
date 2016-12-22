from random import Random

from source.simulation_modules.replication import Replication


class ReplicationTrigger:
    random_number_generator = Random()
    random_number_generator.seed()

    @classmethod
    def set_seed(cls, seed):
        cls.random_number_generator.seed(seed)

    def __init__(self, replication_origin):
        self.replication_origin = replication_origin
        self.start_probability = replication_origin.start_probability
        self.replication_started = False

    def try_to_start(self):
        if not self.replication_started and self.random_float() < self.replication_origin.start_probability:
            self.replication_started = True
            return Replication(self.replication_origin, -1), Replication(self.replication_origin, 1)

        return None, None

    def random_float(self):
        return self.random_number_generator.random()
