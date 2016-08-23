import unittest
from chromosome import Chromosome
from transcription_region import TranscriptionRegion
from transcription import Transcription


class TestChromosomeMethods(unittest.TestCase):

    def setUp(self):
        self.chromosome = Chromosome("c1", [5, 7], [], 20, 1, 4)

    def test_add_transcription_region(self):
        self.chromosome.add_transcription_region(2, 5, 2, 10)
        self.assertIsInstance(self.chromosome.transcription_regions, list)
        transcription_region = self.chromosome.transcription_regions[0]
        self.assertIsInstance(transcription_region, TranscriptionRegion)
        self.assertEqual(transcription_region.chromosome_code, "c1")
        self.assertEqual(transcription_region.transcription_start, 2)
        self.assertEqual(transcription_region.transcription_end, 5)
        self.assertEqual(transcription_region.speed, 2)
        self.assertEqual(transcription_region.delay, 10)

    def test_select_origin(self):
        self.assertEqual(self.chromosome.select_origin(), 5)


class TestTranscriptionMethods(unittest.TestCase):

    def setUp(self):
        self.transcription_region = TranscriptionRegion("c1", 2, 5, 3, 10)
        self.transcription = Transcription(self.transcription_region)

    def test_begin(self):
        self.transcription.begin()
        self.assertEqual(self.transcription.current_position, 2)

    def test_step(self):
        self.transcription.begin()
        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 10)

    def test_finish(self):
        self.transcription.finish()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 11)

if __name__ == '__main__':
    unittest.main()
