#!/usr/bin/env python

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
    chromosome = Chromosome("c_test1", [200000], [], 550000, 50, 10)
    chromosome.add_transcription_region(20000, 30000, 30, 20)

    # simulation setup
    simulation = Simulation(chromosome)
    simulation.begin()

    number_of_steps = 50000
    while number_of_steps > 0:
        simulation.step()
        print(simulation.replication.left_fork, simulation.replication.right_fork)
        print("--------------------------------------------")
        number_of_steps -= 1

if __name__ == "__main__":
    main()
