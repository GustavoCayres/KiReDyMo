from unittest import TestCase
from source.simulation_modules.collision import Collision
from source.simulation_modules.transcription import Transcription
from source.simulation_modules.transcription_region import TranscriptionRegion
from source.simulation_modules.chromosome import Chromosome
from source.simulation_modules.replication import Replication


class TestCollision(TestCase):
    def setUp(self):
        transcription_regions = [TranscriptionRegion(12, 15, 3, 10), TranscriptionRegion(2, 8, 3, 10)]
        self.transcriptions = []
        self.transcriptions.append(Transcription(transcription_regions[0]))
        self.transcriptions[0].begin()
        self.transcriptions.append(Transcription(transcription_regions[1]))
        self.transcriptions[1].begin()

        chromosome = Chromosome("c1", [10], [], 20, 6, 5)
        self.replication = Replication(chromosome)
        self.replication.begin()

    def test_position(self):
        self.assertEqual(Collision.position(1, 5, 77, 5), 1)              # Equal velocities don't lead to collision.
        self.assertEqual(Collision.position(0, 100, 100, -100), 50)       # Opposite directions.
        self.assertEqual(Collision.position(0, 100, 10, 50), 20)          # Same direction.

    def test_verify(self):
        fork, kind = Collision.verify(self.replication, self.transcriptions[0])
        self.assertEqual(fork, "right")
        self.assertEqual(kind, "tail")
        self.assertEqual(self.replication.right_fork, 10)

        fork, kind = Collision.verify(self.replication, self.transcriptions[1])
        self.assertEqual(fork, "left")
        self.assertEqual(kind, "head")
        self.assertEqual(self.replication.left_fork, 4)

    def test_resolve(self):
        Collision.resolve(self.replication, self.transcriptions)
        self.assertEqual(self.replication.left_repair_wait, 5 + 1)
        self.assertIsNone(self.transcriptions[0].current_position)
        self.assertIsNone(self.transcriptions[1].current_position)
