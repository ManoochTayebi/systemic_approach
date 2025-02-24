import matplotlib.pyplot as plt
from Sibylone_equations_class import SibyloneModel
from scipy.integrate import solve_ivp

class PlotResults:
    def plot_results(self, sol, labels):
        plt.figure(figsize=(10, 6))
        for i in range(len(sol.y)):
            if labels[i] in ['Consultants_Inter_Contrat', 'Consultants_Mission']:
                plt.plot(sol.t, sol.y[i], label=labels[i])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of consultants")
        plt.legend()
        plt.title("Sibylone Process Simulation")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    model = SibyloneModel()
    
    # Initial conditions
    initial_conditions = [
        0,  # Sourcing
        0,  # Messaging
        0,  # AKLIFE
        0,  # KLIF
        0,  # RDV1
        0,  # RDV2
        0,  # Proposal
        model.initial_inter_contrat_consultants,  # Consultants_Inter_Contrat
        model.initial_mission_consultants,  # Consultants_Mission
        0,  # Stock_AO
        0,  # Opportunites
        0,  # Candidats_Positionnes
        0   # Presentation_Clients
    ]
    
    # Time points
    t_span = (0, 53)
    t_eval = [i for i in range(54)]
    
    solution = solve_ivp(model.sibylone_process, t_span, initial_conditions, t_eval=t_eval, method='RK45')
    labels = model.get_variable_names()  

    plotter = PlotResults()
    plotter.plot_results(solution, labels)