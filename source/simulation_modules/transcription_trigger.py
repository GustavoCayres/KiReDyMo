from source.simulation_modules.transcription import Transcription


class TranscriptionTrigger:
    def __init__(self, transcription_region):
        self.transcription_region = transcription_region
        self.start_delay = 0

    def try_to_start(self):
        if self.start_delay == 0:
            self.start_delay = self.transcription_region.delay
            return Transcription(self.transcription_region)
        else:
            self.start_delay -= 1
