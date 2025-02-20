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
    

    def extract_variable_labels():
        model = RecruitmentModel()
        return [attr for attr in dir(model) if not attr.startswith("__") and not callable(getattr(model, attr))]

    labels = extract_variable_labels()

    plotter = PlotResults()
    plotter.plot_results(solution, labels=labels)
    