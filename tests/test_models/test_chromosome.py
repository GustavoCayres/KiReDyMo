from unittest import TestCase

from source.modules.database_get import get_chromosome_by_code


class TestChromosome(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = get_chromosome_by_code("c1")