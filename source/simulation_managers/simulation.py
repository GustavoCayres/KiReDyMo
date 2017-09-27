from source.simulation_managers.collision import Collision
from source.simulation_managers.dna_strand import DNAStrand
from source.simulation_managers.encounter import Encounter
from source.simulation_managers.replication_trigger import ReplicationTrigger
from source.simulation_managers.transcription_trigger import TranscriptionTrigger


class Simulation:
    """ Class controlling the overall progress of the simulation. """

    def __init__(self, chromosome, probability_of_origin_trigger, available_resources):
        self.chromosome = chromosome
        self.probability_of_origin_trigger = probability_of_origin_trigger
        self.available_resources = available_resources

        self.dna_strand = DNAStrand(length=len(self.chromosome))
        self.replications = []
        self.transcriptions = []

        self.collision_manager = Collision(chromosome=self.chromosome)
        self.encounter_manager = Encounter(chromosome=self.chromosome)

        self.replication_trigger = ReplicationTrigger(chromosome=self.chromosome,
                                                      strand=self.dna_strand,
                                                      available_resources=self.available_resources)
        self.transcription_triggers = [TranscriptionTrigger(transcription_region=region,
                                                            chromosome=self.chromosome,
                                                            strand=self.dna_strand)
                                       for region in self.chromosome.transcription_regions]

        self.current_step = -3000
        self.maximum_steps = 10000

    def trigger_transcriptions(self):
        for trigger in self.transcription_triggers:
            trigger.try_to_start(self.transcriptions)

    def trigger_replications(self):
        if self.current_step < 0:
            return

        self.replication_trigger.start_random_origin(self.replications,
                                                     self.probability_of_origin_trigger,
                                                     self.current_step)

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
        while not self.dna_strand.is_duplicated() and self.current_step < self.maximum_steps:
            self.step()

        return [self.chromosome.code,
                self.current_step,
                self.collision_manager.head_collisions,
                len(self.chromosome)/(len(self.replication_trigger.origin_trigger_log) + 1),
                self.chromosome.transcription_start_delay,
                len(self.replication_trigger.origin_trigger_log),
                len(self.chromosome.replication_origins),
                self.dna_strand.duplicated_percentage,
                self.replication_trigger.origin_trigger_log]
