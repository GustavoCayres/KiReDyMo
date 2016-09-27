from unittest import TestCase
from source.simulation_modules.chromosome import Chromosome
from source.simulation_modules.transcription_region import TranscriptionRegion


class TestChromosome(TestCase):
    def setUp(self):
        self.chromosome = Chromosome("c1", [5, 7], [], 20, 1, 4)

    def test___init__(self):
        self.assertEqual(self.chromosome.code, "c1")
        self.assertEqual(self.chromosome.replication_origins, [5, 7])
        self.assertEqual(self.chromosome.transcription_regions, [])
        self.assertEqual(self.chromosome.length, 20)
        self.assertEqual(self.chromosome.replication_speed, 1)
        self.assertEqual(self.chromosome.repair_duration, 4)

    def test___str__(self):
        converted_region = str(self.chromosome)
        self.assertEqual(converted_region, "Chromosome: c1\nOrigins: [5, 7]\nLength: 20\n"
                                           "Replication Speed: 1\nRepair Duration: 4\nTranscription Regions: \n")

    def test_add_transcription_region(self):
        self.chromosome.add_transcription_region(2, 5, 2, 10)
        self.assertIsInstance(self.chromosome.transcription_regions, list)
        transcription_region = self.chromosome.transcription_regions[0]
        self.assertIsInstance(transcription_region, TranscriptionRegion)
        self.assertEqual(transcription_region.transcription_start, 2)
        self.assertEqual(transcription_region.transcription_end, 5)
        self.assertEqual(transcription_region.speed, 2)
        self.assertEqual(transcription_region.delay, 10)

    def test_select_origin(self):
        self.assertEqual(self.chromosome.select_origin(), 5)
