from unittest import TestCase
from source.db_modules.database_wrapper import *


class TestTranscriptionRegion(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replication_origin = get_replication_origin_by_chromosome("c1")

    def test___str__(self):
        converted_origin = str(self.replication_origin)
        self.assertEqual(converted_origin, "5")
