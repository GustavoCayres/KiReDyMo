from unittest import TestCase
import unittest
from source.db_modules.database_wrapper import *


class TestChromosome(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = get_chromosome_by_code("c1")

    @unittest.skip("Unnecessary string test.")
    def test___str__(self):
        chromosome_string = str(self.chromosome)
        self.assertEqual(chromosome_string, "Chromosome: c1\nOrganism: test1\nOrigins: \n5 7 \nLength: 20\n"
                                            "Replication Speed: 2\nRepair Duration: 5\nTranscription Regions: \n")
