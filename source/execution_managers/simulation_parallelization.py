from multiprocessing import Pool

from source.execution_managers.parameter_generation import generate_simulation_parameters
from source.simulation_managers.simulation import Simulation


def run_simulation(chromosome):
    return Simulation(chromosome).run()


def run_parallel_simulations(parameter_generation_arguments):
    simulation_parameters = generate_simulation_parameters(**parameter_generation_arguments)
    return Pool().map(run_simulation, simulation_parameters)
