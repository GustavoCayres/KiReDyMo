from unittest import TestCase
from source.models.transcription_region import TranscriptionRegion


class TestTranscriptionRegion(TestCase):
    def setUp(self):
        self.transcription_region = TranscriptionRegion(start=13, end=16, delay=30, speed=1)

    def test___str__(self):
        self.assertEqual(str(self.transcription_region), "(13, 16)")
