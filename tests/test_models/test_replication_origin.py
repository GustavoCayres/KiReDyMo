from unittest import TestCase
from source.models.replication_origin import ReplicationOrigin


class TestReplicationOrigin(TestCase):
    def setUp(self):
        self.origin = ReplicationOrigin(position=10, start_probability=.4)

    def test___str__(self):
        self.assertEqual(str(self.origin), "10")
