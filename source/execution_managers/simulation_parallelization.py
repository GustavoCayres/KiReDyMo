from multiprocessing import Pool

from source.execution_managers.parameter_generation import generate_simulation_parameters
from source.simulation_managers.simulation import Simulation
from source.output_managers.results_output import make_output_directory, write_overall_results


def run_simulation(parameters):

    return Simulation(parameters['chromosome'], parameters['probability_of_origin_trigger']).run()


def run_parallel_simulations(chromosomes,
                             number_of_simulations,
                             number_of_flexible_origins_range,
                             transcription_start_delay_range,
                             replication_repair_duration,
                             is_transcription_active):

    simulation_counter = 0
    for i in range(number_of_simulations):
        for number_of_fl_origins in range(*number_of_flexible_origins_range):
            for transcription_start_delay in range(*transcription_start_delay_range):
                simulation_parameters = generate_simulation_parameters(chromosomes=chromosomes,
                                                                       transcription_start_delay=transcription_start_delay,
                                                                       number_of_flexible_origins=number_of_fl_origins,
                                                                       replication_repair_duration=replication_repair_duration,
                                                                       is_transcription_active=is_transcription_active)
                results = Pool().map(run_simulation, simulation_parameters)
                simulation_counter += 1
                folder_path = make_output_directory(simulation_number=simulation_counter)
                write_overall_results(results=results, folder_path=folder_path)
