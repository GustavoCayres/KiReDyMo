from source.models.base_model import db
from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion


def create_tables():
    db.create_tables([Chromosome, TranscriptionRegion, ReplicationOrigin], safe=True)


def drop_tables():
    db.drop_tables([Chromosome, TranscriptionRegion, ReplicationOrigin], safe=True)
