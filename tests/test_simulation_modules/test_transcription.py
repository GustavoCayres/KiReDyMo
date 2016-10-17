from unittest import TestCase
from source.db_modules.database_wrapper import *
from source.models.transcription_region import TranscriptionRegion
from source.simulation_modules.transcription import Transcription


class TestTranscription(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcription_region = get_transcription_regions_by_chromosome("c1")[1]

    def setUp(self):
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()

    def test_begin(self):
        self.assertEqual(self.transcription.current_position, 13)

    def test_intermediate_step(self):
        """ Tests a step in an intermediate point of the transcription. """

        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.assertEqual(self.transcription.current_position, 14)
        self.assertEqual(self.transcription.delay_wait, 0)

    def test_end_step(self):
        """ Tests a step that leads to ending the transcription. """

        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.transcription.step()
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 7)

    def test_consecutive_steps(self):
        """ Tests taking a step during the delay. """

        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.transcription.step()
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 7)
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 6)

    def test_finish(self):
        self.transcription.finish()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 7)
