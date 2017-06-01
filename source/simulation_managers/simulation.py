from random import Random

from source.simulation_managers.collision import Collision
from source.simulation_managers.dna_strand import DNAStrand
from source.simulation_managers.encounter import Encounter
from source.simulation_managers.replication_trigger import ReplicationTrigger
from source.simulation_managers.transcription_trigger import TranscriptionTrigger


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    PROBABILITY_OF_ORIGIN_START = .007

    def __init__(self, chromosome):
        self.chromosome = chromosome

        self.dna_strand = DNAStrand(length=len(chromosome))
        self.replications = []
        self.transcriptions = []

        self.collision_manager = Collision(chromosome=chromosome)
        self.encounter_manager = Encounter(chromosome=chromosome)

        self.replication_trigger = ReplicationTrigger(chromosome=chromosome,
                                                      strand=self.dna_strand)
        self.transcription_triggers = [TranscriptionTrigger(transcription_region=region,
                                                            chromosome=chromosome)
                                       for region in chromosome.transcription_regions]

        self.current_step = 0
        self.random_generator = Random()
        self.g1_steps = self.random_generator.randrange(2 * self.chromosome.transcription_start_delay)
        self.maximum_steps = 7080 + self.g1_steps

    def trigger_transcriptions(self):
        for trigger in self.transcription_triggers:
            trigger.try_to_start(self.transcriptions)

    def trigger_replications(self):
        if self.current_step < self.g1_steps or \
           self.random_generator.random() >= Simulation.PROBABILITY_OF_ORIGIN_START:
            return

        self.replication_trigger.start_random_origin(self.replications)

    def step(self):
        """ Move one step forward in the simulation, updating the position of each machinery (both for replication and
        for transcription). """

        self.trigger_transcriptions()
        self.trigger_replications()
        self.encounter_manager.resolve(self.replications)
        self.collision_manager.resolve(self.replications, self.transcriptions)

        for replication in self.replications:
            replication.step()

        for transcription in self.transcriptions:
            transcription.step()

        self.current_step += 1

    def run(self):
        while not self.dna_strand.is_duplicated(threshold=1) and self.current_step < self.maximum_steps:
            self.step()

        return self.current_step - self.g1_steps,\
            self.collision_manager.head_collisions,\
            self.collision_manager.tail_collisions,\
            len(self.chromosome)/self.replication_trigger.triggered_origins,\
            self.chromosome.transcription_start_delay,\
            self.replication_trigger.triggered_origins,\
            self.dna_strand.duplicated_percentage
