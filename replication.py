class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.replication_origin = None
        self.replication_left_fork = None
        self.replication_right_fork = None

    def begin(self):
        """ Begins the replication process, which consists in choosing an origin and starting the transcription
         process in each transcription region. """

        self.replication_origin = self.chromosome.select_origin()
        self.replication_left_fork = self.replication_right_fork = self.replication_origin

    def step(self):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        self.replication_left_fork -= self.chromosome.replication_speed
        if self.replication_left_fork < 0:  # verifies if the left replication ended
            self.replication_left_fork = 0

        self.replication_right_fork += self.chromosome.replication_speed
        if self.replication_right_fork >= self.chromosome.length:  # verifies if the right replication ended
            self.replication_right_fork = self.chromosome.length - 1
