import math
from unittest import TestCase

from source.db_modules.database_get import get_chromosome_by_code, get_transcription_regions_by_chromosome
from source.simulation_modules.collision import Collision
from source.simulation_modules.replication import Replication
from source.simulation_modules.transcription import Transcription


class TestCollision(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = get_chromosome_by_code("c1")
        cls.transcription_regions = get_transcription_regions_by_chromosome("c1")

    def setUp(self):
        self.transcriptions = []
        self.transcriptions.append(Transcription(self.transcription_regions[0]))
        self.transcriptions[0].begin()
        self.transcriptions.append(Transcription(self.transcription_regions[1]))
        self.transcriptions[1].begin()

        self.replication = Replication(self.chromosome)
        self.replication.begin()

    def test_position(self):
        self.assertEqual(Collision.position(1, 5, 77, 5), math.inf)       # Equal velocities don't lead to collision.
        self.assertEqual(Collision.position(0, 100, 100, -100), 50)       # Opposite directions.
        self.assertEqual(Collision.position(0, 100, 10, 50), 20)          # Same direction.

    def test_verify(self):
        fork, kind = Collision.verify(self.replication, self.transcriptions[0])
        self.assertEqual(fork, "left")
        self.assertEqual(kind, "head")
        self.assertEqual(self.replication.left_fork, 3)

    def test_resolve(self):
        Collision.resolve(self.replication, self.transcriptions)
        self.assertEqual(self.replication.left_repair_wait, 5 + 1)
        self.assertIsNone(self.transcriptions[0].current_position)
