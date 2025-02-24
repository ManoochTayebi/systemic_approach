################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import matplotlib.pyplot as plt
from example_equations_class import RecruitmentModel

class PlotResults:
    def plot_results(self, sol, labels):
        plt.figure(figsize=(10,6))
        for i in range(len(sol.y)):
            plt.plot(sol.t, sol.y[i], label=labels[i])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of candidates")
        plt.legend()
        plt.title("Recruitment Process Simulation")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    model = RecruitmentModel()

    solution = model.run_simulation()
    labels = model.get_variable_names()  # Get variable names separately
    
    plotter = PlotResults()
    plotter.plot_results(solution, labels=labels)
    