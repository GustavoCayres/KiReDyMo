from unittest import TestCase

from source.models.transcription_region import TranscriptionRegion
from source.simulation_managers.transcription import Transcription
from source.simulation_managers.transcription_trigger import TranscriptionTrigger


class TestTranscriptionTrigger(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_region = TranscriptionRegion(start=0, end=10, delay=5, speed=2)

    def setUp(self):
        self.transcription_trigger = TranscriptionTrigger(self.transcription_region)

    def test_try_to_start(self):
        self.assertIsInstance(self.transcription_trigger.try_to_start(), Transcription)
        self.assertEqual(self.transcription_trigger.start_delay, 5)
        self.assertIsNone(self.transcription_trigger.try_to_start())
        self.assertEqual(self.transcription_trigger.start_delay, 4)
