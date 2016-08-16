from chromosome import Chromosome


class Simulation:
    """ Class responsible for controlling the steps of the replication process. """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.replication_origin = None
        self.replication_left_fork = None
        self.replication_right_fork = None
        self.transcriptions_current_positions = {}   # key is the transcription region,
        # value is the integer representing the position

    def begin_replication(self):
        """ Begin the replication process, which consists in choosing an origin and starting the transcription
         process in each transcription region. """

        self.replication_origin = self.chromosome.select_origin()
        self.replication_left_fork = self.replication_right_fork = self.replication_origin
        self.begin_transcriptions()

    def begin_transcriptions(self):
        """ Begin transcription in each transcription region. """

        for transcription_region in self.chromosome.transcription_regions:
            key = transcription_region
            self.transcriptions_current_positions[key] = transcription_region.starting_point()

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        self.replication_left_fork -= self.chromosome.replication_speed()
        self.replication_right_fork += self.chromosome.replication_speed()
        for key in self.transcriptions_current_positions:
            self.transcriptions_current_positions[key] += key.transcription_speed()

# very simple test example
c1 = Chromosome(1, [5], [], 10)
c1.add_transcription_region(6, 7, 1, 10)
s = Simulation(c1)
s.begin_replication()
i = 0
while i < 5:
    print(s.replication_left_fork)
    s.step()
    i += 1
