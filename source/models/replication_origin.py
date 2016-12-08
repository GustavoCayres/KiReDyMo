class ReplicationOrigin:

    def __init__(self, position, start_probability):
        self.position = position
        self.start_probability = start_probability

    def __str__(self):
        return str(self.position)
