import unittest
from unittest import TestCase
from source.db_modules.database_seed import DatabaseSeed
from source.db_modules.database_import import DatabaseImport


@unittest.skip("ORM Filler test")
class TestDatabaseImport(TestCase):
    def setUp(self):
        db = DatabaseSeed('./test_db/test_db.sqlite')
        db.drop_tables()
        db.create_tables()
        db.insert_organism("Test organism")
        db.insert_chromosomes("./test_input/Test-organism_chromosome1.txt", 2, 2)
        db.insert_replication_origins(10, "ToChr1")
        db.insert_transcription_regions("./test_input/ToChr1_regions.txt", 1, 150)
        db.close()

        self.db = DatabaseImport('./test_db/test_db.sqlite')

    def test_import_origins_by_chromosome(self):
        origins = self.db.import_origins_by_chromosome("ToChr1")
        self.assertIsInstance(origins, list)
        self.assertEqual(origins, [10])

    def test_import_regions_by_chromosome(self):
        self.fail()

    def test_import_chromosome_by_organism(self):
        self.fail()

    def test_close(self):
        self.fail()

    def tearDown(self):
        db = DatabaseSeed('./test_db/test_db.sqlite')
        db.drop_tables()
        db.close()

        self.db.close()
