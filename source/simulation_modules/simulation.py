from source.simulation_modules.replication import Replication
from source.simulation_modules.transcription import Transcription
from source.simulation_modules.collision import Collision
import random


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    total_duration = 0

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

        Collision.resolve(self.replication, self.transcriptions)

        self.replication.step()
        for transcription in self.transcriptions:
            transcription.step()

    @staticmethod
    def run(chromosome):
        simulation = Simulation(chromosome)
        starting_step = simulation.decide_starting_step(.3)

        # print simulated chromosome
        print(str(chromosome) + "\n")

        print("Simulation of chromosome started at step: " + str(starting_step) + "\n")

        simulation.begin()
        steps = 1
        while simulation.replication.left_fork is not None or simulation.replication.right_fork is not None:
            steps += 1
            if steps <= starting_step:
                continue
            simulation.step()
            print(simulation.replication.left_fork, simulation.replication.right_fork)
            print("--------------------------------------------")
        print("Duration: " + str(steps) + "\n")

        if steps > Simulation.total_duration:
            Simulation.total_duration = steps

    @staticmethod
    def decide_starting_step(start_probability):
        starting_step = 1
        while random.random() >= start_probability:
            starting_step += 1

        return starting_step
