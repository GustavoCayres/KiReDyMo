from source.simulation_managers.simulation import Simulation


def run_simulation(parameters):
    chromosome = parameters[0]
    simulation_number = parameters[1]

    simulation_duration, head_collisions, tail_collisions, repair_duration,\
        transcription_delay, origins = Simulation(chromosome).run()
    result = "{}\t{}\t{}\t{}\t{}\t{}\t\n".format(simulation_duration,
                                                 head_collisions, tail_collisions,
                                                 repair_duration, transcription_delay,
                                                 [str(origin) for origin in origins])

    with open("output/" + chromosome.code + "_" + str(simulation_number) + "_results.txt", 'w') as output_file:
        output_file.write(result)
