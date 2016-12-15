import random

from source.simulation_modules.replication import Replication


class ReplicationTrigger:
    def __init__(self, replication_origin):
        self.replication_origin = replication_origin
        self.start_probability = replication_origin.start_probability
        self.replication_started = False

    def try_to_start(self):
        if not self.replication_started:
            if random.random() < self.replication_origin.start_probability:
                self.replication_started = True
                return Replication(self.replication_origin)
