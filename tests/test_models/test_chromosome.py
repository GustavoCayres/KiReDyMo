from unittest import TestCase

from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion


class TestChromosome(TestCase):
    def setUp(self):
        self.chromosome = Chromosome(code="C1", length=10, replication_speed=2, organism="Test organism")

    def test___str__(self):
        self.assertEqual(str(self.chromosome),
                         "Chromosome: C1\nOrganism: Test organism\nOrigins: \n\n"
                         "Length: 10 bases\nReplication Speed: 2 bases per second\nTranscription Regions: \n\n")

    def test_update_attributes(self):
        self.assertEqual(self.chromosome.replication_origins, [])
        self.assertEqual(self.chromosome.transcription_regions, [])
        origins = [ReplicationOrigin(1, 1, 10, 2), ReplicationOrigin(6, 1, 10, 40)]
        regions = [TranscriptionRegion(1, 3, 2, 4)]

        self.chromosome.transcription_regions = regions
        self.chromosome.update_attributes(replication_origins=origins)
        self.assertEqual(self.chromosome.replication_origins, origins)

        self.chromosome.update_attributes(replication_repair_duration=37)
        for origin in self.chromosome.replication_origins:
            self.assertEqual(origin.replication_repair_duration, 37)

        self.chromosome.update_attributes(transcription_start_delay=11)
        for region in self.chromosome.transcription_regions:
            self.assertEqual(region.delay, 11)
