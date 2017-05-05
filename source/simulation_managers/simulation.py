from source.simulation_managers.collision_verification import CollisionVerifier
from source.simulation_managers.encounter import Encounter
from source.simulation_managers.replication_trigger import ReplicationTrigger
from source.simulation_managers.transcription_trigger import TranscriptionTrigger
from source.simulation_managers.dna_strand import DNAStrand
from random import Random


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    PROBABILITY_OF_ORIGIN_START = 1
    MAXIMUM_STEPS = 1000000
    G1_STEPS = 1000

    def __init__(self, chromosome):
        self.chromosome = chromosome

        self.dna_strand = DNAStrand(length=chromosome.length)
        self.replications = []
        self.transcriptions = []

        self.collision_verifier = CollisionVerifier(chromosome, self.replications, self.transcriptions)
        self.encounter_manager = Encounter(chromosome)

        self.replication_trigger = ReplicationTrigger(chromosome.replication_origins)
        self.transcription_triggers = [TranscriptionTrigger(region) for region in chromosome.transcription_regions]

        self.current_step = 0
        self.random_generator = Random()

    def trigger_transcriptions(self):
        for trigger in self.transcription_triggers:
            transcription = trigger.try_to_start()
            if transcription is not None:
                self.transcriptions.append(transcription)

    def trigger_replications(self):
        if self.random_generator.random() < 1 - Simulation.PROBABILITY_OF_ORIGIN_START or\
           self.current_step < Simulation.G1_STEPS:
            return

        left_replication, right_replication = self.replication_trigger.start_random_origin()
        if left_replication is not None and right_replication is not None:
            self.replications.append(left_replication)
            self.replications.append(right_replication)

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        self.trigger_transcriptions()
        self.trigger_replications()

        self.collision_verifier.verify_collisions()

        for replication in self.replications:
            replication.step()

        for transcription in self.transcriptions:
            transcription.step(collision_verifier=self.collision_verifier)

        self.current_step += 1

    def run(self):
        while not self.dna_strand.is_duplicated() and self.current_step < Simulation.MAXIMUM_STEPS:
            self.step()

        return self.current_step - Simulation.G1_STEPS,\
            self.collision_verifier.head_collisions,\
            self.collision_verifier.tail_collisions,\
            self.chromosome.replication_origins[0].replication_repair_duration,\
            self.chromosome.transcription_regions[0].delay,\
            [str(origin) for origin in self.chromosome.replication_origins]
