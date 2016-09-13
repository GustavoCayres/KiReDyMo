import unittest
from source.chromosome import Chromosome
from source.transcription_region import TranscriptionRegion
from source.transcription import Transcription
from source.replication import Replication
from source.simulation import Simulation


class TestChromosomeMethods(unittest.TestCase):
    """ Basic tests. """

    def setUp(self):
        self.chromosome = Chromosome("c1", [5, 7], [], 20, 1, 4)

    def test_add_transcription_region(self):
        self.chromosome.add_transcription_region(2, 5, 2, 10)
        self.assertIsInstance(self.chromosome.transcription_regions, list)
        transcription_region = self.chromosome.transcription_regions[0]
        self.assertIsInstance(transcription_region, TranscriptionRegion)
        self.assertEqual(transcription_region.chromosome_code, "c1")
        self.assertEqual(transcription_region.transcription_start, 2)
        self.assertEqual(transcription_region.transcription_end, 5)
        self.assertEqual(transcription_region.speed, 2)
        self.assertEqual(transcription_region.delay, 10)

    def test_select_origin(self):
        self.assertEqual(self.chromosome.select_origin(), 5)


class TestTranscriptionBasicMethods(unittest.TestCase):
    """ Basic tests. """

    def setUp(self):
        self.transcription_region = TranscriptionRegion("c1", 2, 5, 3, 10)
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


class TestTranscriptionStepMethod(unittest.TestCase):

    def test_intermediate_step(self):
        """ Tests a step in an intermediate point of the transcription. """

        self.transcription_region = TranscriptionRegion("c1", 10, 2, 3, 15)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()
        self.assertEqual(self.transcription.direction, -1)
        self.transcription.step()
        self.assertEqual(self.transcription.current_position, 7)
        self.assertEqual(self.transcription.delay_wait, 0)

    def test_end_step(self):
        """ Tests a step that leads to ending the transcription. """

        self.transcription_region = TranscriptionRegion("c1", 2, 5, 3, 10)
        self.transcription = Transcription(self.transcription_region)
        self.transcription.begin()
        self.assertEqual(self.transcription.direction, 1)
        self.transcription.step()
        self.assertIsNone(self.transcription.current_position)
        self.assertEqual(self.transcription.delay_wait, 10)

    def test_consecutive_steps(self):
        """ Tests taking a step during the delay. """

        self.transcription_region = TranscriptionRegion("c1", 2, 5, 2, 10)
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


class TestReplicationMethods(unittest.TestCase):

    def setUp(self):
        self.chromosome = Chromosome("c1", [5], [], 8, 1, 5)
        self.replication = Replication(self.chromosome)
        self.replication.begin()

    def test_begin(self):
        self.assertEqual(self.replication.origin, 5)
        self.assertEqual(self.replication.origin, self.replication.left_fork)
        self.assertEqual(self.replication.left_fork, self.replication.right_fork)

    def test_step(self):
        self.replication.step()
        self.assertEqual(self.replication.origin, 5)
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 6)
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 2)
        self.assertIsNone(self.replication.right_fork)
        self.replication.step()
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 0)
        self.replication.step()
        self.assertIsNone(self.replication.left_fork)
        self.assertIsNone(self.replication.right_fork)

    def test_pause(self):
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 6)
        self.replication.pause("left")
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 7)
        self.replication.pause("right")
        self.replication.step()
        self.assertEqual(self.replication.left_fork, 4)
        self.assertEqual(self.replication.right_fork, 7)


class TestSimulationMethods(unittest.TestCase):

    def setUp(self):
        self.chromosome = Chromosome("c1", [5], [], 8, 1, 5)
        self.chromosome.add_transcription_region(2, 3, 1, 10)
        self.chromosome.add_transcription_region(8, 7, 1, 10)
        self.simulation = Simulation(self.chromosome)

    def test_begin(self):
        self.simulation.begin()
        self.assertEqual(self.simulation.replication.origin, 5)
        self.assertEqual(self.simulation.transcriptions[0].current_position, 2)
        self.assertEqual(self.simulation.transcriptions[1].current_position, 8)

if __name__ == '__main__':
    unittest.main()
