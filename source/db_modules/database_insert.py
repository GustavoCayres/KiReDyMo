from source.models.chromosome import Chromosome
from source.models.replication_origin import ReplicationOrigin
from source.models.transcription_region import TranscriptionRegion


def insert_chromosome(code, length, replication_speed, repair_duration, organism):
    Chromosome.insert(code=code, length=length, replication_speed=replication_speed,
                      repair_duration=repair_duration, organism=organism).execute()


def insert_replication_origin(**kwargs):
    """ Insert a replication origin with the specifieds
    {position, start_probability, chromosome}
    into the specified chromosome. """
    ReplicationOrigin.insert(kwargs).execute()


def insert_transcription_region(start, end, speed, delay, chromosome):
    TranscriptionRegion.insert(start=start, end=end, speed=speed, delay=delay, chromosome=chromosome).execute()


def insert_genes_as_regions(genes):
    genes.sort(key=lambda x: x[0])
    previous_gene = genes[0]
    start = previous_gene[0]
    end = previous_gene[1]
    for gene in genes[1:]:
        if previous_gene[5] != gene[5]:  # different polycistronic region
            if previous_gene[5] == "(-)":
                TranscriptionRegion.create(start=end, end=start, speed=previous_gene[2], delay=previous_gene[3],
                                           chromosome=previous_gene[4])
            else:
                TranscriptionRegion.create(start=start, end=end, speed=previous_gene[2], delay=previous_gene[3],
                                           chromosome=previous_gene[4])
            start = gene[0]

        end = gene[1]  # update region's end
        previous_gene = gene
    if previous_gene[5] == "(-)":
        TranscriptionRegion.create(start=end, end=start, speed=previous_gene[2], delay=previous_gene[3],
                                   chromosome=previous_gene[4])
    else:
        TranscriptionRegion.create(start=start, end=end, speed=previous_gene[2], delay=previous_gene[3],
                                   chromosome=previous_gene[4])


def insert_transcription_regions_from_file(file_name, speed, delay):
    """ Imports the chromosome's transcription regions from txt file 'file_name'.
        The file format must be:
        [Gene ID]   [Transcript ID] [Organism]  [Genomic Location(s)]
        where the separation are TABs.                                            """

    genes = []
    with open(file_name, 'r') as file:
        header_line_as_list = next(file).split("\t")
        data_index = -1                 # let's find what column holds our desired data
        for index, tag in enumerate(header_line_as_list):
            if tag == "[Genomic Location(s)]":
                data_index = index

        for line in file:
            line_as_list = line.split("\t")
            data = line_as_list[data_index].split()

            chromosome = data[0].replace(':', '')
            start = data[1].replace(',', '')
            end = data[3].replace(',', '')
            direction = data[4]
            genes.append((int(start), int(end), int(speed), int(delay), chromosome, direction))

    if len(genes) > 0:
        insert_genes_as_regions(genes)


def insert_chromosomes_from_file(file_name, replication_speed, repair_duration):
    """ Imports the chromosomes from txt file 'file_name'.
        The file format contain columns with headers [Length], [Description] and [Sequence ID]
        where the separation are TABs.                                                          """

    with open(file_name, 'r') as file:
        header_line_as_list = next(file).split("\t")
        code_index = -1         # let's find what column holds our desired data
        length_index = -1
        organism_index = -1
        for index, tag in enumerate(header_line_as_list):
            if tag == "[Length]":
                length_index = index
            elif tag == "[Sequence ID]":
                code_index = index
            elif tag == "[Description]":
                organism_index = index

        chromosome_amount = 0
        for line in file:
            chromosome_amount += 1
            line_as_list = line.split("\t")

            length = line_as_list[length_index].replace(',', '')
            code = line_as_list[code_index]
            organism = line_as_list[organism_index]
            Chromosome.insert(code=code, length=length, replication_speed=replication_speed,
                              repair_duration=repair_duration, organism=organism).execute()
    return chromosome_amount
