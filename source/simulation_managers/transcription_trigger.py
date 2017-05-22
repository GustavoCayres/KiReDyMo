from source.simulation_managers.transcription import Transcription


class TranscriptionTrigger:
    def __init__(self, transcription_region, chromosome):
        self.chromosome = chromosome
        self.transcription_region = transcription_region
        self.remaining_start_delay = 0

    def try_to_start(self, transcriptions):
        if self.remaining_start_delay == 0:
            self.remaining_start_delay = self.chromosome.transcription_start_delay
            transcriptions.append(Transcription(region=self.transcription_region,
                                                speed=self.chromosome.transcription_speed))
        else:
            self.remaining_start_delay -= 1
