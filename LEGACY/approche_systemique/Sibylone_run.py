import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from Sibylone_equations_class import SibyloneModel

# Load simulation parameters
SIMULATION_DURATION = 80  # Time units (weeks)
PLOTTED_VARIABLES = ["Sourcing", "Consultants en Mission", "Consultant en Inter-contrat"]

class PlotResults:
    def __init__(self, labels):
        self.labels = labels
        self.indices_to_plot = [labels.index(var) for var in PLOTTED_VARIABLES if var in labels]

    def plot_results(self, sol, time_points):
        plt.figure(figsize=(10, 6))
        for idx in self.indices_to_plot:
            plt.plot(time_points, sol[:, idx], label=self.labels[idx])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of candidates")
        plt.legend()
        plt.title("Sibylone Recruitment Process Simulation")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    model = SibyloneModel()

    # Get initial conditions
    initial_state = model.get_initial_conditions()

    # Time points for simulation
    time_points = np.linspace(0, SIMULATION_DURATION, SIMULATION_DURATION + 1)

    # Run simulation
    solution = odeint(model.sibylone_model, initial_state, time_points)

    # Get variable names
    labels = model.get_variable_names()
    
    # Plot results
    plotter = PlotResults(labels)
    plotter.plot_results(solution, time_points)
