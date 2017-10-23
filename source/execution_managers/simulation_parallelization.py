from multiprocessing import Pool

from source.execution_managers.parameter_generation import generate_simulation_parameters, generate_origins
from source.simulation_managers.simulation import Simulation
from source.output_managers.results_output import make_output_directory, write_overall_results,\
    make_simulation_directory


def run_simulation(parameters):

    return Simulation(**parameters).run()


def run_parallel_simulations(chromosomes,
                             N_range,
                             number_of_simulations,
                             bases_between_origins_range,
                             transcription_start_delay_range,
                             replication_repair_duration,
                             is_transcription_active):

    make_output_directory()
    simulation_number = 1
    pool = Pool()
    for bases_between_origins in range(*bases_between_origins_range):
        for chromosome in chromosomes:
            chromosome.flexible_origins = []
            chromosome.flexible_origins += generate_origins(chromosome=chromosome,
                                                            bases_between_origins=bases_between_origins)
            chromosome.flexible_origins += chromosome.constitutive_origins

        for available_resources in range(*N_range):
            simulation_parameters = generate_simulation_parameters(chromosomes=chromosomes,
                                                                   transcription_start_delay=None,
                                                                   replication_repair_duration=replication_repair_duration,
                                                                   available_resources=available_resources,
                                                                   is_transcription_active=is_transcription_active)
            for i in range(number_of_simulations):
                    results = pool.map(run_simulation, simulation_parameters)
                    folder_path = make_simulation_directory(simulation_number=simulation_number)
                    write_overall_results(results=results, folder_path=folder_path, bbo=bases_between_origins)
                    simulation_number += 1
