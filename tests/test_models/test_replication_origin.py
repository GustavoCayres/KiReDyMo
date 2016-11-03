from unittest import TestCase
from source.models.replication_origin import ReplicationOrigin


class TestTranscriptionRegion(TestCase):

    def setUp(self):
        self.query = ReplicationOrigin.select().where(ReplicationOrigin.chromosome == "c1")

    def test___str__(self):
        replication_origins = set()
        for origin in self.query:
            replication_origins |= {str(origin)}
        self.assertSetEqual({'0', '7'}, replication_origins)
