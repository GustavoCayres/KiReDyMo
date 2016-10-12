from unittest import TestCase

from source.models.transcription_region import TranscriptionRegion
from source.simulation_modules.transcription import Transcription


class TestTranscription(TestCase):
    def setUp(self):
        self.transcription_region = TranscriptionRegion(2, 5, 3, 10)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()

    def test_begin(self):
        self.assertEqual(self.transcription.current_position, 2)

    def test_intermediate_step(self):
        """ Tests a step in an intermediate point of the transcription. """

        self.transcription_region = TranscriptionRegion(10, 2, 3, 15)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()
        self.assertEqual(self.transcription.direction, -1)
        self.transcription.step()
        self.assertEqual(self.transcription.current_position, 7)
        self.assertEqual(self.transcription.delay_wait, 0)

    def test_end_step(self):
        """ Tests a step that leads to ending the transcription. """

        self.transcription_region = TranscriptionRegion(2, 5, 3, 10)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()
        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 10)

    def test_consecutive_steps(self):
        """ Tests taking a step during the delay. """

        self.transcription_region = TranscriptionRegion(2, 5, 2, 10)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()
        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 10)
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 9)

    def test_finish(self):
        self.transcription.finish()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 10)
