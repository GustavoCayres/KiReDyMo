import math
from unittest import TestCase

from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion
from source.simulation_modules.collision import Collision
from source.simulation_modules.replication import Replication
from source.simulation_modules.transcription import Transcription


class TestCollision(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_regions = [TranscriptionRegion(start=2, end=6, speed=2, delay=10),
                                     TranscriptionRegion(start=12, end=16, speed=2, delay=10),
                                     TranscriptionRegion(start=7, end=9, speed=2, delay=10)]
        cls.replication_origins = [ReplicationOrigin(position=10, score=0.1, replication_speed=5,
                                                     replication_repair_duration=5)]

    def setUp(self):
        self.transcriptions = [Transcription(region) for region in self.transcription_regions]
        self.replications = [Replication(self.replication_origins[0], -1), Replication(self.replication_origins[0], 1)]
        self.collision = Collision()

    def test_position(self):
        self.assertEqual(Collision.position(1, 5, 77, 5), math.inf)       # Equal velocities don't lead to collision.
        self.assertEqual(Collision.position(0, 100, 100, -100), 50)       # Opposite directions.
        self.assertEqual(Collision.position(0, 100, 10, 50), 20)          # Same direction.

    def test_verify_no_collision(self):
        kind = self.collision.verify(self.replications[0], self.transcriptions[0])
        self.assertIsNone(kind)

    def test_verify_tail_collision(self):
        kind = self.collision.verify(self.replications[1], self.transcriptions[1])
        self.assertEqual(kind, "tail")

    def test_verify_head_collision(self):
        kind = self.collision.verify(self.replications[0], self.transcriptions[2])
        self.assertEqual(kind, "head")

    def test_collision_with_stopped_replication(self):
        self.replications[0].pause()
        self.replications[0].step()
        self.collision.resolve(self.replications, self.transcriptions)
        self.assertEqual(self.replications[0].current_repair_wait, 5 - 1)

    def test_resolve(self):
        self.collision.resolve(self.replications, self.transcriptions)
        self.assertEqual(self.replications[0].current_repair_wait, 5)
        self.assertEqual(len(self.transcriptions), 1)
