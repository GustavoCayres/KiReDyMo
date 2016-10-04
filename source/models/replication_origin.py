from peewee import *

from .base_model import BaseModel
from .chromosome import Chromosome


class ReplicationOrigin(BaseModel):

    origin = IntegerField()
    chromosome = ForeignKeyField(Chromosome, related_name="origins")

    class Meta:
        primary_key = CompositeKey('origin', 'chromosome')
