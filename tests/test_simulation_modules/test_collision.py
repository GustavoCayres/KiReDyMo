import math
from unittest import TestCase

from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.collision import Collision
from source.simulation_modules.replication import Replication
from source.simulation_modules.transcription import Transcription
from source.models.chromosome import Chromosome
from source.models.transcription_region import TranscriptionRegion


class TestCollision(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = Chromosome(code="c1", length=20, organism="TtChr1", replication_speed=5)
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=2, end=6, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=12, end=16, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=9, end=7, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=18, end=17, speed=2, delay=10))

    def setUp(self):
        self.transcriptions = [Transcription(region) for region in self.chromosome.transcription_regions]
        self.replications = [Transcription(region) for region in self.chromosome.transcription_regions]

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
