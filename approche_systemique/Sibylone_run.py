import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from Sibylone_equations_class import SibyloneModel
import numpy as np

class PlotResults:
    def plot_results(self, sol, labels):
        plt.figure(figsize=(10,6))
        for i in range(len(sol.y)):
            if labels[i] in ["Consultants_Inter_Contrat", "Consultants_Mission"]:
                plt.plot(sol.t, sol.y[i], label=labels[i])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of consultants")
        plt.legend()
        plt.title("Sibylone Process Simulation")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    model = SibyloneModel()

    # Initial conditions for the variables
    initial_conditions = [0] * len(model.get_variable_names())

    # INTER-CONTRAT REPORTS
    initial_conditions[model.get_variable_names().index("Consultants_Inter_Contrat")] = model.initial_inter_contrat_consultants

    # Time points
    t = np.linspace(0, 52, 53) # Ensure that the start and end time are included in the array

    # Solve ODE
    sol = solve_ivp(model.sibylone_process, (t[0], t[-1]), initial_conditions, t_eval=t)

    # Plot results
    plot_results = PlotResults()
    plot_results.plot_results(sol, model.get_variable_names())