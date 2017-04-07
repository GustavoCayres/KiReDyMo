class Completition:
    def __init__(self):
        self.replication_encounters = []

    def save_replication_encountering_replication(self, replication_1, replication_2):
        if replication_1.direction > 0:
            self.replication_encounters.append((replication_1.origin, replication_2.origin))
        else:
            self.replication_encounters.append((replication_2.origin, replication_1.origin))

    def save_replication_encountering_end(self, replication):
        if replication.direction > 0:
            self.replication_encounters.append((replication.origin, -1))
        else:
            self.replication_encounters.append((-1, replication.origin))

    def done(self):
        if len(self.replication_encounters) == 0:
            return False

        return {origin_tuple[0] for origin_tuple in self.replication_encounters} ==\
               {origin_tuple[1] for origin_tuple in self.replication_encounters}
