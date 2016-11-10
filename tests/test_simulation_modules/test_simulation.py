from unittest import TestCase

from source.modules.database_get import get_chromosome_by_code
from source.simulation_modules.simulation import Simulation


class TestSimulation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = get_chromosome_by_code("c1")

    def setUp(self):
        self.simulation = Simulation(self.chromosome)
        self.simulation.begin()

    def test_begin(self):
        self.assertEqual(self.simulation.replication.origin.position, 5)
        self.assertSetEqual({self.simulation.transcriptions[0].current_position,
                             self.simulation.transcriptions[1].current_position}, {3, 13})
