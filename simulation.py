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
            self.transcriptions_current_positions[key] = transcription_region.transcription_start

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        self.replication_left_fork -= self.chromosome.replication_speed
        self.replication_right_fork += self.chromosome.replication_speed
        for key in self.transcriptions_current_positions:                        # each key is a transcription region
            self.transcriptions_current_positions[key] += key.adjusted_transcription_speed()

    def validate_state(self):
        """ Tests the bounds of the simulation, such as chromosome's and transcription regions' lengths. """

        valid = True
        for region, position in self.transcriptions_current_positions.items():
            if position < region.transcription_start or position > region.transcription_end:
                valid = False


        return valid
        # return (self.replication_left_fork >= 0) and (self.replication_right_fork < self.chromosome.length)


def main():

    # chromosome setup
    chromosome = Chromosome(1, [5], [], 10, 1)
    chromosome.add_transcription_region(6, 7, 1, 10)

    # simulation setup
    simulation = Simulation(chromosome)
    simulation.begin_replication()


    i = 0
    while i < 5:
        print(simulation.replication_left_fork)
        simulation.step()
        i += 1

if __name__ == "__main__":
    main()
