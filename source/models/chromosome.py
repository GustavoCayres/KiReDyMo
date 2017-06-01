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

        self.__constitutive_origins = []
        self.__flexible_origins = []

    @property
    def constitutive_origins(self):
        return self.__constitutive_origins

    @constitutive_origins.setter
    def constitutive_origins(self, origins):
        self.__constitutive_origins = origins
        self.replication_origins = sorted(self.__constitutive_origins + self.__flexible_origins)

    @property
    def flexible_origins(self):
        return self.__flexible_origins

    @flexible_origins.setter
    def flexible_origins(self, origins):
        self.__flexible_origins = origins
        self.replication_origins = sorted(self.__constitutive_origins + self.__flexible_origins)

    def __len__(self):
        return self.length
