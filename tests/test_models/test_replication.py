from unittest import TestCase
from source.db_modules.database_wrapper import *
from source.simulation_modules.replication import Replication


class TestReplication(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = get_chromosome_by_code("c1")

    def setUp(self):
        self.replication = Replication(self.chromosome)
        self.replication.begin()

    def test_begin(self):
        self.assertEqual(self.replication.origin.position, 5)
        self.assertEqual(self.replication.origin.position, self.replication.left_fork)
        self.assertEqual(self.replication.left_fork, self.replication.right_fork)

    def test_step(self):
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 3)
        self.assertEqual(self.replication.right_fork, 7)
        self.replication.step()
        self.replication.step()
        self.assertIsNone(self.replication.left_fork)
        self.assertEqual(self.replication.right_fork, 11)
        self.replication.step()
        self.replication.step()
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.right_fork, 19)
        self.replication.step()
        self.assertIsNone(self.replication.right_fork)

    def test_pause(self):
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 3)
        self.assertEqual(self.replication.right_fork, 7)
        self.replication.pause("left")
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 3)
        self.assertEqual(self.replication.right_fork, 9)
        self.replication.pause("right")
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 3)
        self.assertEqual(self.replication.right_fork, 9)
        self.replication.step()
        self.replication.step()
        self.replication.step()
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 1)
