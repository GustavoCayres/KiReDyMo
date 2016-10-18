from source.models.base_model import *
from source.models.chromosome import Chromosome


class TranscriptionRegion(BaseModel):
    """ Organizes the properties of each transcript region,
        allowing different transcription speeds for each transcription region. """

    start = IntegerField()
    end = IntegerField()
    speed = IntegerField()
    delay = IntegerField()
    chromosome = ForeignKeyField(Chromosome, related_name='transcription_regions')

    class Meta:
        primary_key = CompositeKey('start', 'end', 'chromosome')

    def __str__(self):
        return "(" + str(self.start) + ", " + str(self.end) + ")"
