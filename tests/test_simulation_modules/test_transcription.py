from unittest import TestCase

from source.models.transcription_region import TranscriptionRegion
from source.simulation_managers.transcription import Transcription


class TestTranscription(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_region = TranscriptionRegion(12, 16, 2, 10)

    def setUp(self):
        self.transcription = Transcription(self.transcription_region)

    def test_begin(self):
        self.assertEqual(self.transcription.current_position, 12)

    def test_step(self):
        """ Tests a step in an intermediate point of the transcription. """

        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.assertEqual(self.transcription.current_position, 14)

    def test_leaving_region(self):
        self.assertFalse(self.transcription.is_leaving_region())
        self.transcription.step()
        self.assertFalse(self.transcription.is_leaving_region())
        self.transcription.step()
        self.assertTrue(self.transcription.is_leaving_region())
