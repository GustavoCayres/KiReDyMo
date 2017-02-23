class Chromosome:
    """ Model of each chromosome. """

    def __init__(self, code, length, organism):
        self.code = code
        self.length = length
        self.organism = organism
        self.replication_origins = []
        self.transcription_regions = []

    def update_attributes(self, **kwargs):
        for key in kwargs:
            value = kwargs[key]
            if key == 'replication_origins':
                self.replication_origins = value

        for key in kwargs:
            value = kwargs[key]
            if key == 'transcription_start_delay':
                for region in self.transcription_regions:
                    region.delay = value
            elif key == 'replication_repair_duration':
                for origin in self.replication_origins:
                    origin.replication_repair_duration = value

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
