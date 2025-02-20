################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from Sibylone_equations_class import SibyloneModel

class PlotResults:
    def plot_results(self, sol, labels):
        plt.figure(figsize=(10,6))
        for i in range(len(sol)):
            plt.plot(np.arange(0, len(sol[0]), 1), sol[:,i], label=labels[i])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of candidates")
        plt.legend()
        plt.title("Sibylone Process Simulation")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    model = SibyloneModel()
    t = np.linspace(0, 52, 53)  # Simulate for 1 year (52 weeks)

    solution = model.run_simulation(t)

    def extract_variable_labels():
        return [attr for attr in dir(model) if not attr.startswith("__") and not callable(getattr(model, attr))]

    labels = extract_variable_labels()

    plotter = PlotResults()
    plotter.plot_results(solution, labels=labels)