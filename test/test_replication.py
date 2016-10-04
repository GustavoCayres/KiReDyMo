from unittest import TestCase

from source.models.chromosome import Chromosome
from source.simulation_modules.replication import Replication


class TestReplication(TestCase):
    def setUp(self):
        self.chromosome = Chromosome("c1", [5], [], 8, 1, 5)
        self.replication = Replication(self.chromosome)
        self.replication.begin()

    def test_begin(self):
        self.assertEqual(self.replication.origin, 5)
        self.assertEqual(self.replication.origin, self.replication.left_fork)
        self.assertEqual(self.replication.left_fork, self.replication.right_fork)

    def test_step(self):
        self.replication.step()
        self.assertEqual(self.replication.origin, 5)
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 6)
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 2)
        self.assertIsNone(self.replication.right_fork)
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 0)
        self.replication.step()
        self.assertIsNone(self.replication.left_fork)
        self.assertIsNone(self.replication.right_fork)

    def test_pause(self):
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 6)
        self.replication.pause("left")
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 7)
        self.replication.pause("right")
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 7)
