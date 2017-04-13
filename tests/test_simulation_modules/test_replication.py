from unittest import TestCase

from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.replication import Replication


class TestReplication(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.replication_origin = ReplicationOrigin(position=5, score=0.1,
                                                   replication_speed=2, replication_repair_duration=3)
        cls.replication_origin_with_instant_repair = ReplicationOrigin(position=5,
                                                                       score=1,
                                                                       replication_speed=2,
                                                                       replication_repair_duration=0)

    def setUp(self):
        self.replication = Replication(self.replication_origin, -1)

    def test_step(self):
        self.replication.step()
        self.assertEqual(self.replication.fork_position, 3)
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.fork_position, -1)

    def test_pause(self):
        self.replication.step()
        self.assertEqual(self.replication.fork_position, 3)
        self.replication.pause()
        self.replication.step()
        self.assertEqual(self.replication.fork_position, 3)
        self.replication.step()
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.fork_position, 1)

    def test_pause_with_instant_resume(self):
        replication_with_instant_repair = Replication(self.replication_origin_with_instant_repair, -1)

        replication_with_instant_repair.step()
        self.assertEqual(replication_with_instant_repair.fork_position, 3)
        replication_with_instant_repair.pause()
        replication_with_instant_repair.step()
        self.assertEqual(replication_with_instant_repair.fork_position, 1)
