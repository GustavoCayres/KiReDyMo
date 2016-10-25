from unittest import TestCase

from source.db_modules.database_get import get_transcription_regions_by_chromosome


class TestTranscriptionRegion(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_region = get_transcription_regions_by_chromosome("c1")[1]

    def test___str__(self):
        converted_region = str(self.transcription_region)
        self.assertEqual(converted_region, "(13, 16)")
