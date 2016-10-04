from peewee import *

from source.models.base_model import BaseModel
from source.models.organism import Organism


class Chromosome(BaseModel):
    """ Class containing data on the chromosome """

    code = CharField(max_length=10, primary_key=True)
    length = IntegerField()
    replication_speed = IntegerField()
    repair_duration = IntegerField()
    organism = ForeignKeyField(Organism, related_name="chromosomes")

    def __str__(self):
        list_representation = list()
        list_representation.append("Chromosome: " + self.code)
        list_representation.append("Origins: " + str(self.replication_origins))
        list_representation.append("Length: " + str(self.length))
        list_representation.append("Replication Speed: " + str(self.replication_speed))
        list_representation.append("Repair Duration: " + str(self.repair_duration))
        list_representation.append("Transcription Regions: ")

        regions = ""
        for region in self.transcription_regions:

            regions += str(region)
        list_representation.append(regions)

        return "\n".join(list_representation)
