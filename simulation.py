from chromosome import Chromosome
from replication import Replication
from transcription import Transcription
from collision import Collision


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.replication = Replication(self.chromosome)
        self.transcriptions = []
        for transcription_region in self.chromosome.transcription_regions:
            self.transcriptions.append(Transcription(transcription_region))

    def begin(self):
        """ Begins the simulation, activating the replication and all the transcriptions. """

        self.replication.begin()
        for transcription in self.transcriptions:
            transcription.begin()

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        Collision.resolve_collisions(self.replication, self.transcriptions)

        self.replication.step()
        for transcription in self.transcriptions:
            transcription.step()


def main():

    # chromosome setup
    chromosome = Chromosome(1, [5], [], 10, 1)
    chromosome.add_transcription_region(9, 2, 1, 10)

    # simulation setup
    simulation = Simulation(chromosome)
    simulation.begin()

    number_of_steps = 50
    while number_of_steps > 0:
        print(simulation.transcriptions[0].current_position)

        simulation.step()
        number_of_steps -= 1

if __name__ == "__main__":
    main()
