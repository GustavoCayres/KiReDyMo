from source.simulation_modules.collision import Collision
from source.simulation_modules.encounter import Encounter
from source.simulation_modules.replication_trigger import ReplicationTrigger
from source.simulation_modules.transcription_trigger import TranscriptionTrigger


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    def __init__(self, chromosome):
        self.current_step = 0
        self.collision_manager = Collision()
        self.encounter_manager = Encounter(chromosome)
        self.chromosome = chromosome

        self.replication_triggers = [ReplicationTrigger(origin) for origin in chromosome.replication_origins]
        self.replications = []

        self.transcription_triggers = [TranscriptionTrigger(region) for region in chromosome.transcription_regions]
        self.transcriptions = []

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        for trigger in self.transcription_triggers:
            transcription = trigger.try_to_start()
            if transcription is not None:
                self.transcriptions.append(transcription)
        for trigger in self.replication_triggers:
            left_replication, right_replication = trigger.try_to_start()
            if left_replication is not None and right_replication is not None:
                self.replications.append(left_replication)
                self.replications.append(right_replication)

        done = self.encounter_manager.resolve(self.replications)
        self.collision_manager.resolve(self.replications, self.transcriptions)

        for replication in self.replications:
            replication.step()

        for transcription in self.transcriptions:
            transcription.step()

        self.current_step += 1

        return done

    def run(self):
        done = False
        while not done:
            done = self.step()

        return self.current_step,\
            self.collision_manager.head_collisions,\
            self.collision_manager.tail_collisions,\
            self.chromosome.replication_origins[0].replication_repair_duration,\
            self.chromosome.transcription_regions[0].delay,\
            self.chromosome.replication_origins
