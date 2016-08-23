import unittest
from chromosome import Chromosome
from transcription_region import TranscriptionRegion


class TestChromosomeMethods(unittest.TestCase):

    def setUp(self):
        self.chromosome = Chromosome("c1", [5, 7], [], 20, 1, 4)

    def test_add_transcription_region(self):
        self.chromosome.add_transcription_region(2, 5, 2, 10)
        self.assertIsInstance(self.chromosome.transcription_regions, list)
        transcription_region = self.chromosome.transcription_regions[0]
        self.assertIsInstance(transcription_region, TranscriptionRegion)
        self.assertEqual(transcription_region.chromosome_code, self.chromosome.code)
        self.assertEqual(transcription_region.transcription_start, 2)
        self.assertEqual(transcription_region.transcription_end, 5)
        self.assertEqual(transcription_region.speed, 2)
        self.assertEqual(transcription_region.delay, 10)

    def test_select_origin(self):
        self.assertEqual(self.chromosome.select_origin(), self.chromosome.replication_origins[0])

if __name__ == '__main__':
    unittest.main()
