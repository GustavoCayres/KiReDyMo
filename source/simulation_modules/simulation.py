from source.simulation_modules.collision import Collision
from source.simulation_modules.encounter import Encounter
from source.simulation_modules.replication import Replication
from source.simulation_modules.transcription import Transcription
# noinspection PyUnresolvedReferences
from source.models.replication_origin import ReplicationOrigin


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    def __init__(self, chromosome):

        self.current_step = 0

        self.replications = []
        for replication_origin in chromosome.replication_origins:
            self.replications.append(Replication(replication_origin))

        self.transcription_regions = [[x, 0] for x in chromosome.transcription_regions]

        self.transcriptions = []

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

        self.transcriptions[:] = [x for x in self.transcriptions if x.current_position is not None]

        for transcription in self.transcriptions:
                transcription.step()

        for item in self.transcription_regions:
            if item[1] == 0:
                self.transcriptions.append(Transcription(item[0]))
                item[1] = item[0].delay
            else:
                item[1] -= 1

        return done

    def run(self):
        done = False
        while not done:
            done = self.step()
        print("Duration: " + str(self.current_step) + "\n")
