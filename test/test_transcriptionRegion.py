from unittest import TestCase
from source.transcription_region import TranscriptionRegion


class TestTranscriptionRegion(TestCase):
    """ Basic tests. """

    def setUp(self):
        self.transcription_region = TranscriptionRegion(2, 5, 3, 10)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()

    def test_begin(self):
        self.assertEqual(self.transcription.current_position, 2)

    def test_step(self):
        # Look for specific class.
        pass

    def test_finish(self):
        self.transcription.finish()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 11)
