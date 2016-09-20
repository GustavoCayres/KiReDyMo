from unittest import TestCase
from source.chromosome import Chromosome
from source.simulation import Simulation


class TestSimulation(TestCase):
    def setUp(self):
        self.chromosome = Chromosome("c1", [5], [], 8, 1, 5)
        self.chromosome.add_transcription_region(2, 3, 1, 10)
        self.chromosome.add_transcription_region(8, 7, 1, 10)
        self.simulation = Simulation(self.chromosome)

    def test_begin(self):
        self.simulation.begin()
        self.assertEqual(self.simulation.replication.origin, 5)
        self.assertEqual(self.simulation.transcriptions[0].current_position, 2)
        self.assertEqual(self.simulation.transcriptions[1].current_position, 8)
