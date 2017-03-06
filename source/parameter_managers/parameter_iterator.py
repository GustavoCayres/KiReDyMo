class ParameterIterator:
    def __init__(self, chromosome, s_phase_dur, replication_repair_duration_range, transcription_start_delay_range):
        self.last_simulation_duration = None
        self.s_phase_duration = s_phase_dur
        self.chromosome = chromosome
        self.replication_repair_duration_range = replication_repair_duration_range
        self.transcription_start_delay_range = transcription_start_delay_range

    def __iter__(self):
        for y in range(*self.transcription_start_delay_range):
            self.last_simulation_duration = None
            x = None
            binary_search_range = [self.replication_repair_duration_range[0], self.replication_repair_duration_range[1]]

            for i in range(10):
                if self.last_simulation_duration is not None:
                    if self.last_simulation_duration >= self.s_phase_duration:
                        binary_search_range[1] = x
                    else:
                        binary_search_range[0] = x
                x = int((binary_search_range[0] + binary_search_range[1]) / 2)

                self.chromosome.update_attributes(transcription_start_delay=y, replication_repair_duration=x)
                yield self.chromosome
