#!/usr/bin/env python

from .chromosome import Chromosome
from .replication import Replication
from .transcription import Transcription
from .collision import Collision


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

    # TODO: Seed the database with a toy organism.
    # chromosome setup
    chromosome = Chromosome('c1', [5], [], 10, 4, 2)
    chromosome.add_transcription_region(2, 3, 1, 10)
    chromosome.add_transcription_region(8, 7, 1, 10)
    print(chromosome)

    # simulation setup
    simulation = Simulation(chromosome)
    simulation.begin()
    steps = 0
    while simulation.replication.left_fork is not None or simulation.replication.right_fork is not None:
        simulation.step()
        steps += 1
        print(simulation.replication.left_fork, simulation.replication.right_fork)
        print("--------------------------------------------")
    print("Total steps: ", steps)

if __name__ == "__main__":
    main()
