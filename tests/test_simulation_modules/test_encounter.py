from unittest import TestCase

from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.encounter import Encounter
from source.simulation_modules.replication import Replication


class TestEncounter(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = Chromosome(code="c1", length=20, organism="TtChr1", replication_speed=5)
        cls.chromosome.replication_origins.append(ReplicationOrigin(position=15, score=0.1,
                                                                    replication_speed=5, replication_repair_duration=5))
        cls.chromosome.replication_origins.append(ReplicationOrigin(position=5, score=0.1,
                                                                    replication_speed=5, replication_repair_duration=5))

    def setUp(self):
        self.replications = []
        self.replications.append(Replication(self.chromosome.replication_origins[0], -1))
        self.replications.append(Replication(self.chromosome.replication_origins[0], 1))
        self.replications.append(Replication(self.chromosome.replication_origins[1], -1))
        self.replications.append(Replication(self.chromosome.replication_origins[1], 1))

        self.encounter = Encounter(self.chromosome)

    def test_resolve(self):
        self.encounter.resolve(self.replications)
        self.assertEqual(self.replications[0].fork_position, 5)
        self.assertEqual(len(self.replications), 1)
