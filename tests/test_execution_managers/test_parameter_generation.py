from unittest import TestCase

from source.execution_managers.parameter_generation import generate_origins
from source.models.chromosome import Chromosome


class TestParameterGeneration(TestCase):
    def setUp(self):
        self.chromosome = Chromosome(code="C1",
                                     length=10,
                                     organism="Test organism",
                                     replication_speed=10,
                                     transcription_speed=5,
                                     replication_repair_duration=10,
                                     transcription_start_delay=10)

    def test_generate_too_many_origins(self):
        origins = generate_origins(chromosome=self.chromosome, number_of_origins=100, score_of_new_origins=10)
        self.assertEqual(len(origins), len(self.chromosome))
