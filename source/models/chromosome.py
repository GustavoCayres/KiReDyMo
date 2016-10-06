from peewee import *

from source.models.base_model import BaseModel


class Chromosome(BaseModel):
    """ Class containing data on the chromosome """

    code = CharField(max_length=10, primary_key=True)
    length = IntegerField()
    replication_speed = IntegerField()
    repair_duration = IntegerField()
    organism = CharField(max_length=30)

    def __str__(self):
        text = list()
        text.append("Chromosome: " + self.code)
        text.append("Organism: " + self.organism)

        text.append("Origins: ")
        origins = ""
        for origin in self.replication_origins:
            origins += str(origin) + " "
        text.append(origins)

        text.append("Length: " + str(self.length))
        text.append("Replication Speed: " + str(self.replication_speed))
        text.append("Repair Duration: " + str(self.repair_duration))

        text.append("Transcription Regions: ")
        regions = ""
        for region in self.transcription_regions:
            regions += str(region) + " "
        text.append(regions)

        return "\n".join(text)
