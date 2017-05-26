class Chromosome:
    """ Model of each chromosome. """

    def __init__(self, **kwargs):
        self.code = kwargs['code']
        self.length = kwargs['length']
        self.organism = kwargs['organism']
        self.replication_speed = kwargs['replication_speed']
        self.transcription_speed = kwargs['transcription_speed']
        self.replication_repair_duration = kwargs['replication_repair_duration']
        self.transcription_start_delay = kwargs['transcription_start_delay']
        self.replication_origins = []
        self.transcription_regions = []

    def __len__(self):
        return self.length

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
        text.append("Replication Speed: " + str(self.replication_speed) + " bases per second")
        text.append("Transcription Regions: ")
        regions = ""
        for region in self.transcription_regions:
            regions += str(region) + " "
        text.append(regions)

        return "\n".join(text) + "\n"
