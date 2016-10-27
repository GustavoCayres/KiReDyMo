from source.models.base_model import *
from source.models.chromosome import Chromosome


class ReplicationOrigin(BaseModel):

    position = IntegerField()
    start_probability = FloatField()
    chromosome = ForeignKeyField(Chromosome, related_name='replication_origins')

    class Meta:
        primary_key = CompositeKey('position', 'chromosome')

    def __str__(self):
        return str(self.position)
