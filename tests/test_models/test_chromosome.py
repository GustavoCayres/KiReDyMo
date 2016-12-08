from unittest import TestCase
from source.models.chromosome import Chromosome


class TestChromosome(TestCase):
    def setUp(self):
        self.chromosome = Chromosome(code="C1", length=10, replication_speed=2, organism="Test organism")

    def test___str__(self):
        self.assertEqual(str(self.chromosome),
                         "Chromosome: C1\nOrganism: Test organism\nOrigins: \n\n"
                         "Length: 10 bases\nReplication Speed: 2 b/s\nTranscription Regions: \n\n")
