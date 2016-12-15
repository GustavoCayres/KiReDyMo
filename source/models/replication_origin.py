class ReplicationOrigin:
    def __init__(self, position, start_probability, replication_speed, replication_repair_duration):
        self.position = position
        self.start_probability = start_probability
        self.replication_speed = replication_speed
        self.replication_repair_duration = replication_repair_duration

    def __str__(self):
        return str(self.position)
