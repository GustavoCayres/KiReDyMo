class Chromosome:
    """ Model of each chromosome. """

    def __init__(self, code, length, organism):
        self.code = code
        self.length = length
        self.organism = organism
        self.replication_origins = []
        self.transcription_regions = []

    def __str__(self):
        text = list()
        text.append("Chromosome: " + self.code)
        text.append("Organism: " + self.organism)

        text.append("Origins: ")
        origins = ""
        for origin in self.replication_origins:
            origins += str(origin) + " "
        text.append(origins)

        text.append("Length: " + str(self.length) + " bases")
        text.append("Transcription Regions: ")
        regions = ""
        for region in self.transcription_regions:
            regions += str(region) + " "
        text.append(regions)

        return "\n".join(text) + "\n"
