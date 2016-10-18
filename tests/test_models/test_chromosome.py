from unittest import TestCase
from source.db_modules.database_wrapper import *


class TestChromosome(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = get_chromosome_by_code("c1")
