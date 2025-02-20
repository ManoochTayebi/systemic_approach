################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import matplotlib.pyplot as plt

class PlotResults:
    def plot_results(self, sol, labels):
        plt.figure(figsize=(10,6))
        for i in range(len(sol.y)):
            plt.plot(sol.t, sol.y[i], label=labels[i])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of candidates")
        plt.legend()
        plt.title("Sibylone Process Simulation")
        plt.grid()
        plt.show()