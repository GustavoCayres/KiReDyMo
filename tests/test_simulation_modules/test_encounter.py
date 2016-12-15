from unittest import TestCase

from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.simulation_modules.encounter import Encounter
from source.simulation_modules.replication import Replication


class TestEncounter(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chromosome = Chromosome(code="c1", length=20, organism="TtChr1")
        cls.chromosome.replication_origins.append(ReplicationOrigin(position=16, start_probability=0.1,
                                                                    replication_speed=5, replication_repair_duration=5))
        cls.chromosome.replication_origins.append(ReplicationOrigin(position=5, start_probability=0.1,
                                                                    replication_speed=5, replication_repair_duration=5))

    def setUp(self):
        self.replications = [Replication(origin) for origin in self.chromosome.replication_origins]
        self.encounter = Encounter(self.chromosome.length)

    def test_resolve(self):
        self.encounter.resolve(self.replications)
        self.assertIsNone(self.replications[1].left_fork)
        self.assertIsNone(self.replications[0].right_fork)
        self.assertEqual(self.replications[0].left_fork, 16)
