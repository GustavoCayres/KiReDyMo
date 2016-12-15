from unittest import TestCase

from source.simulation_modules.simulation import Simulation
from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion


class TestSimulation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = Chromosome(code="c1", length=20, organism="TtChr1")
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=2, end=6, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=12, end=16, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=7, end=9, speed=2, delay=10))
        cls.chromosome.replication_origins.append(ReplicationOrigin(position=10, start_probability=0.1,
                                                                    replication_speed=5, replication_repair_duration=5))

    def setUp(self):
        self.simulation = Simulation(self.chromosome, 10, 10)

    def test_run(self):
        total_steps = self.simulation.run()[0]
        self.assertGreaterEqual(total_steps, 2)

    def test_step(self):
        pass
