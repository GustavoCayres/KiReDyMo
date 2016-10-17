from peewee import *

from .base_model import BaseModel
from .chromosome import Chromosome


class ReplicationOrigin(BaseModel):

    position = IntegerField()
    chromosome = ForeignKeyField(Chromosome, related_name='replication_origins')

    class Meta:
        primary_key = CompositeKey('position', 'chromosome')

    def __str__(self):
        return str(self.position)
