from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion


def get_chromosome_by_code(code):
    return Chromosome.get(Chromosome.code == code)


def get_transcription_regions_by_chromosome(chromosome_code):
    transcription_regions = []
    for transcription_region in TranscriptionRegion.select().where(TranscriptionRegion.chromosome == chromosome_code):
        transcription_regions.append(transcription_region)
    return transcription_regions


def get_replication_origin_by_chromosome(chromosome_code):
    return ReplicationOrigin.select().where(ReplicationOrigin.chromosome == chromosome_code).\
        order_by(ReplicationOrigin.position).get()
