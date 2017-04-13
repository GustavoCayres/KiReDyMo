from unittest import TestCase

from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.replication_trigger import ReplicationTrigger


class TestReplicationTrigger(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replication_origin = ReplicationOrigin(position=10, score=.5,
                                                   replication_repair_duration=10, replication_speed=5)
        ReplicationTrigger.set_seed(1)

    def setUp(self):
        self.replication_trigger_1 = ReplicationTrigger(self.replication_origin)
        self.replication_trigger_2 = ReplicationTrigger(self.replication_origin)

    def test_random(self):
        self.assertNotAlmostEqual(self.replication_trigger_1.random_float(), self.replication_trigger_2.random_float())

    def test_try_to_start(self):
        pass
