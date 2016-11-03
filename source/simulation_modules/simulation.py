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

        self.current_step = None

        self.replications = []
        for replication_origin in self.chromosome.replication_origins:
            self.replications.append(Replication(replication_origin))

        self.transcriptions = []
        for transcription_region in self.chromosome.transcription_regions:
            self.transcriptions.append(Transcription(transcription_region))

    def begin(self):
        """ Begins the simulation, activating the replication and all the transcriptions. """

        self.current_step = 0

        for transcription in self.transcriptions:
            transcription.begin()

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        self.current_step += 1

        Encounter.resolve(self.replications)

        done = True
        for replication in self.replications:
            Collision.resolve(replication, self.transcriptions)
            replication.step(self.current_step)
            if not replication.triggered or not (replication.left_fork is None and replication.right_fork is None):
                done = False

        for transcription in self.transcriptions:
            transcription.step()

        return done

    def run(self):

        # print simulated chromosome
        print(str(self.chromosome) + "\n")

        self.begin()
        done = False
        while not done:
            done = self.step()
        print("Duration: " + str(self.current_step) + "\n")
