class Replication:
    """ Controls the replication process of a chromosome. """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.origin = None
        self.left_fork = None
        self.right_fork = None

    def begin(self):
        """ Begins the replication process, which consists in choosing an origin and starting the transcription
         process in each transcription region. """

        self.origin = self.chromosome.select_origin()
        self.left_fork = self.right_fork = self.origin

    def step(self):
        """ Takes a step in the replication, taking into account the chromosome's boundaries. """

        self.left_fork -= self.chromosome.replication_speed
        if self.left_fork < 0:  # verifies if the left replication ended
            self.left_fork = 0

        self.right_fork += self.chromosome.replication_speed
        if self.right_fork >= self.chromosome.length:  # verifies if the right replication ended
            self.right_fork = self.chromosome.length - 1
