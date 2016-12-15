from unittest import TestCase

from source.simulation_modules.transcription import Transcription
from source.models.transcription_region import TranscriptionRegion


class TestTranscription(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_region = TranscriptionRegion(12, 16, 2, 10)

    def setUp(self):
        self.transcription = Transcription(self.transcription_region)

    def test_begin(self):
        self.assertEqual(self.transcription.current_position, 12)

    def test_intermediate_step(self):
        """ Tests a step in an intermediate point of the transcription. """

        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.assertEqual(self.transcription.current_position, 14)

    def test_end_step(self):
        """ Tests a step that leads to ending the transcription. """

        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
