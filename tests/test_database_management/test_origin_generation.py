from unittest import TestCase

from source.database_management.origin_generation import *
from source.models.chromosome import Chromosome
from source.models.transcription_region import TranscriptionRegion


class TestOriginGeneration(TestCase):
    def setUp(self):
        self.chromosome = Chromosome("TestChr", 10, "Test organism")
        self.chromosome.transcription_regions.append(TranscriptionRegion(0, 4, 1, 5))
        self.chromosome.transcription_regions.append(TranscriptionRegion(6, 9, 1, 5))

    def test_generate_randomized_origins_in_inversions(self):
        origins = generate_randomized_origins_in_inversions(self.chromosome, 2, 10)
        for origin in origins:
            self.assertIn(origin[0], [0, 4, 6, 9])
