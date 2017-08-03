from multiprocessing import Pool

from source.execution_managers.parameter_generation import generate_simulation_parameters, generate_origins
from source.simulation_managers.simulation import Simulation
from source.output_managers.results_output import make_output_directory, write_overall_results,\
    make_simulation_directory


def run_simulation(parameters):

    return Simulation(parameters['chromosome'], parameters['probability_of_origin_trigger']).run()


def run_parallel_simulations(chromosomes,
                             number_of_simulations,
                             bases_between_origins_range,
                             transcription_start_delay_range,
                             replication_repair_duration,
                             is_transcription_active):

    make_output_directory()
    simulation_parameters = []
    pool = Pool()
    for i in range(number_of_simulations):
        for chromosome in chromosomes:
            chromosome.flexible_origins = generate_origins(chromosome=chromosome,
                                                           bases_between_origins=bases_between_origins_range[0])
        for transcription_start_delay in range(*transcription_start_delay_range):
            simulation_parameters += generate_simulation_parameters(chromosomes=chromosomes,
                                                                    transcription_start_delay=transcription_start_delay,
                                                                    replication_repair_duration=replication_repair_duration,
                                                                    is_transcription_active=is_transcription_active)
        results = pool.map(run_simulation, simulation_parameters)
        folder_path = make_simulation_directory(simulation_number=i+1)
        write_overall_results(results=results, folder_path=folder_path)
        simulation_parameters = []
