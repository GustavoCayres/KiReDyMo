from source.simulation_modules.collision import Collision
from source.simulation_modules.encounter import Encounter
from source.simulation_modules.replication_trigger import ReplicationTrigger
from source.simulation_modules.transcription_trigger import TranscriptionTrigger


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    def __init__(self, chromosome, replication_repair_duration, transcription_start_delay):
        self.current_step = 0
        self.collision_manager = Collision()
        self.encounter_manager = Encounter(chromosome.length)
        self.chromosome = chromosome

        self.replication_triggers = \
            [ReplicationTrigger(origin, chromosome.replication_speed, replication_repair_duration)
             for origin in chromosome.replication_origins]
        self.replications = []

        self.transcription_triggers = [TranscriptionTrigger(region) for region in chromosome.transcription_regions]

        self.transcription_start_delay = transcription_start_delay
        self.transcriptions = []

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        for trigger in self.transcription_triggers:
            transcription = trigger.try_to_start()
            self.transcriptions.append(transcription) if transcription is not None else None
        for trigger in self.replication_triggers:
            replication = trigger.try_to_start()
            self.replications.append(replication) if replication is not None else None
        done = self.encounter_manager.resolve(self.replications)
        for replication in self.replications:
            self.collision_manager.resolve(replication, self.transcriptions)

        self.transcriptions[:] = [x for x in self.transcriptions if x.current_position is not None]
        self.replications[:] = [x for x in self.replications if x.left_fork is not None or x.right_fork is not None]

        for replication in self.replications:
            replication.step(self.current_step)

        for transcription in self.transcriptions:
            transcription.step()

        self.current_step += 1

        return done

    def run(self):
        done = False
        while not done:
            done = self.step()
        return self.current_step, self.collision_manager.head_collisions, self.collision_manager.tail_collisions
