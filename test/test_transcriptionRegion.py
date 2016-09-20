from unittest import TestCase
from source.transcription_region import TranscriptionRegion


class TestTranscriptionRegion(TestCase):
    def setUp(self):
        self.transcription_region = TranscriptionRegion(20, 80, 5, 7)

    def test___init__(self):
        self.assertEqual(self.transcription_region.transcription_start, 20)
        self.assertEqual(self.transcription_region.transcription_end, 80)
        self.assertEqual(self.transcription_region.speed, 5)
        self.assertEqual(self.transcription_region.delay, 7)

    def test___str__(self):
        converted_region = str(self.transcription_region)
        self.assertEqual(converted_region, "(20, 80)")
