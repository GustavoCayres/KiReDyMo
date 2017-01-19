import copy


def chromosomes_with_update_attributes(chromosome):
    chromosomes_list = []

    for replication_repair_duration in range(0, 8 * 3600, 8 * 360):
        for transcription_start_delay in range(2000, 10, -200):
            chromosome_copy = copy.deepcopy(chromosome)
            for region in chromosome_copy.transcription_regions:
                setattr(region, 'delay', transcription_start_delay)
            for origin in chromosome_copy.replication_origins:
                setattr(origin, 'replication_repair_duration', replication_repair_duration)

            chromosomes_list.append(chromosome_copy)

    return chromosomes_list
