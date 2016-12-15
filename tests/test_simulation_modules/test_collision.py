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
        cls.chromosome = Chromosome(code="c1", length=20, organism="TtChr1")
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=2, end=6, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=12, end=16, speed=2, delay=10))
        cls.chromosome.transcription_regions.append(TranscriptionRegion(start=7, end=9, speed=2, delay=10))
        cls.chromosome.replication_origins.append(ReplicationOrigin(position=10, start_probability=0.1,
                                                                    replication_speed=5, replication_repair_duration=5))

    def setUp(self):
        self.transcriptions = [Transcription(region) for region in self.chromosome.transcription_regions]
        self.replications = [Replication(origin) for origin in self.chromosome.replication_origins]
        self.collision = Collision()

    def test_position(self):
        self.assertEqual(Collision.position(1, 5, 77, 5), math.inf)       # Equal velocities don't lead to collision.
        self.assertEqual(Collision.position(0, 100, 100, -100), 50)       # Opposite directions.
        self.assertEqual(Collision.position(0, 100, 10, 50), 20)          # Same direction.

    def test_verify_no_collision(self):
        fork, kind = Collision.verify(self.replications[0], self.transcriptions[0])
        self.assertIsNone(fork)
        self.assertIsNone(kind)

    def test_verify_tail_collision(self):
        fork, kind = Collision.verify(self.replications[0], self.transcriptions[1])
        self.assertEqual(fork, "right")
        self.assertEqual(kind, "tail")

    def test_verify_head_collision(self):
        fork, kind = Collision.verify(self.replications[0], self.transcriptions[2])
        self.assertEqual(fork, "left")
        self.assertEqual(kind, "head")

    def test_resolve(self):
        self.collision.resolve(self.replications[0], self.transcriptions)
        self.assertEqual(self.replications[0].left_repair_wait, 5 + 1)
        self.assertIsNone(self.transcriptions[2].current_position)
