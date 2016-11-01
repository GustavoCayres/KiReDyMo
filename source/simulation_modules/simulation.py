from source.simulation_modules.collision import Collision
from source.simulation_modules.encounter import Encounter
from source.simulation_modules.replication import Replication
from source.simulation_modules.transcription import Transcription
# noinspection PyUnresolvedReferences
from source.models.replication_origin import ReplicationOrigin


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    def __init__(self, chromosome):
        self.chromosome = chromosome

        self.replications = []
        for replication_origin in self.chromosome.replication_origins:
            self.replications.append(Replication(replication_origin))

        self.transcriptions = []
        for transcription_region in self.chromosome.transcription_regions:
            self.transcriptions.append(Transcription(transcription_region))

    def begin(self):
        """ Begins the simulation, activating the replication and all the transcriptions. """

        for replication in self.replications:
            replication.begin()

        for transcription in self.transcriptions:
            transcription.begin()

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        Encounter.resolve(self.replications)

        done = True
        for replication in self.replications:
            Collision.resolve(replication, self.transcriptions)
            replication.step()
            if replication.left_fork is not None or replication.right_fork is not None:
                done = False

        for transcription in self.transcriptions:
            transcription.step()

        return done

    @staticmethod
    def run(chromosome):
        simulation = Simulation(chromosome)

        # print simulated chromosome
        print(str(chromosome) + "\n")

        simulation.begin()
        steps = 1
        done = False
        while not done:
            steps += 1
            done = simulation.step()
            print(simulation.replications[0].left_fork, simulation.replications[0].right_fork)
            print("--------------------------------------------")
        print("Duration: " + str(steps) + "\n")
