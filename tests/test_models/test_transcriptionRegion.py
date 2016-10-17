from unittest import TestCase
from source.db_modules.database_wrapper import *


class TestTranscriptionRegion(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_region = get_transcription_region_by_chromosome("c1")

    def test___str__(self):
        converted_region = str(self.transcription_region)
        self.assertEqual(converted_region, "(13, 16)")
