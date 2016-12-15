from unittest import TestCase
from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.replication import Replication


class TestReplication(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.replication_origin = ReplicationOrigin(position=5, start_probability=0.1,
                                                   replication_speed=2, replication_repair_duration=3)

    def setUp(self):
        self.replication = Replication(self.replication_origin)

    def test_step(self):
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 3)
        self.assertEqual(self.replication.right_fork, 7)
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.left_fork, -1)
        self.assertEqual(self.replication.right_fork, 11)

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
        self.assertEqual(self.replication.left_fork, 1)
        self.assertEqual(self.replication.right_fork, 9)
