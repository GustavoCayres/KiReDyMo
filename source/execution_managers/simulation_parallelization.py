from multiprocessing import Pool
from source.execution_managers.simulation_execution import run_simulation
from source.execution_managers.parameter_generation import generate_simulation_parameters


def run_parallel_simulations(parameter_generation_arguments):
    simulation_parameters = generate_simulation_parameters(**parameter_generation_arguments)
    Pool().map(run_simulation, simulation_parameters)
