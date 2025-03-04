################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import networkx as nx

################################################################################

class RecruitmentModel:
    def __init__(self, r_s, r_m, r_nr, r_ref, r_ak, r_akneg, r_k, r_kneg, r_r1, r_r2neg, r_r2, r_r3neg, r_p, r_pref, r_c, sourcing_rate=60, time_span=(0, 53), time_steps=100):
        self.sourcing_rate = sourcing_rate
        self.time_span = time_span
        self.t_eval = np.linspace(time_span[0], time_span[1], time_steps)
        
        # Process rates
        self.r_s = r_s      # Non retenu
        self.r_m = r_m      # Message envoyé
        self.r_nr = r_nr    # Pas de retour
        self.r_ref = r_ref  # Rejeté
        self.r_ak = r_ak    # Réponse acceptée
        self.r_akneg = r_akneg  # AKLIF négatif
        self.r_k = r_k      # KLIF positif
        self.r_kneg = r_kneg  # RDV1 rejeté
        self.r_r1 = r_r1    # RDV1 positif
        self.r_r2neg = r_r2neg  # RDV2 négatif
        self.r_r2 = r_r2    # RDV2 positif
        self.r_r3neg = r_r3neg  # RDV3 négatif
        self.r_p = r_p      # Passe en proposition
        self.r_pref = r_pref  # Proposition rejetée
        self.r_c = r_c      # Accepté

    def sourcing_function(self, t):
        return self.sourcing_rate

    def recruitment_process(self, t, y):
        S, M, AK, K, R1, R2, P, C = y
        f_s = self.sourcing_function(t)
        
        dS_dt = f_s - self.r_s * S - self.r_m * S
        dM_dt = self.r_m * S - self.r_nr * M - self.r_ref * M - self.r_ak * M
        dAK_dt = self.r_ak * M - self.r_akneg * AK - self.r_k * AK
        dK_dt = self.r_k * AK - self.r_kneg * K - self.r_r1 * K
        dR1_dt = self.r_r1 * K - self.r_r2neg * R1 - self.r_r2 * R1
        dR2_dt = self.r_r2 * R1 - self.r_r3neg * R2 - self.r_p * R2
        dP_dt = self.r_p * R2 - self.r_pref * P - self.r_c * P
        dC_dt = self.r_c * P
        
        return [dS_dt, dM_dt, dAK_dt, dK_dt, dR1_dt, dR2_dt, dP_dt, dC_dt]

    def run_simulation(self):
        y0 = [10, 0, 0, 0, 0, 0, 0, 0]
        sol = solve_ivp(self.recruitment_process, self.time_span, y0, t_eval=self.t_eval)
        return sol

    def plot_results(self, sol):
        plt.figure(figsize=(10,6))
        labels = ["Sourcé", "Messaged", "AKLIFé", "KLIF", "RDV1", "RDV2", "Proposal", "Consultants"]
        for i in range(len(sol.y)):
            plt.plot(sol.t, sol.y[i], label=labels[i])
        plt.xlabel("Time (weeks)")
        plt.ylabel("Number of candidates")
        plt.legend()
        plt.title("Recruitment Process Simulation")
        plt.grid()
        plt.show()

    def plot_causal_loop_diagram(self):
        G = nx.DiGraph()

        # Define nodes
        nodes = [
            "Sourcing (f_s)", "Sourcé", "Messaged", "AKLIFé", "KLIF", "RDV1", "RDV2", "Proposal", "Consultants",
            "Non retenu", "Pas de retour", "Rejeté", "AKLIF négatif", "RDV1 rejeté", "RDV2 négatif", "RDV3 négatif", "Proposition rejetée"
        ]
        G.add_nodes_from(nodes)

        # Define edges with process rates
        edges = [
            ("Sourcing (f_s)", "Sourcé", "f_s"),  
            ("Sourcé", "Messaged", f"r_m = {self.r_m}"),  
            ("Sourcé", "Non retenu", f"r_s = {self.r_s}"),  
            ("Messaged", "Pas de retour", f"r_nr = {self.r_nr}"),  
            ("Messaged", "Rejeté", f"r_ref = {self.r_ref}"),  
            ("Messaged", "AKLIFé", f"r_ak = {self.r_ak}"),  
            ("AKLIFé", "AKLIF négatif", f"r_akneg = {self.r_akneg}"),  
            ("AKLIFé", "KLIF", f"r_k = {self.r_k}"),  
            ("KLIF", "RDV1", f"r_r1 = {self.r_r1}"),  
            ("KLIF", "RDV1 rejeté", f"r_kneg = {self.r_kneg}"),  
            ("RDV1", "RDV2", f"r_r2 = {self.r_r2}"),  
            ("RDV1", "RDV2 négatif", f"r_r2neg = {self.r_r2neg}"),  
            ("RDV2", "Proposal", f"r_p = {self.r_p}"),  
            ("RDV2", "RDV3 négatif", f"r_r3neg = {self.r_r3neg}"),  
            ("Proposal", "Consultants", f"r_c = {self.r_c}"),  
            ("Proposal", "Proposition rejetée", f"r_pref = {self.r_pref}")
        ]

        G.add_edges_from([(u, v) for u, v, _ in edges])

        # Define layout (aligned positioning)
        pos = {
            "Sourcing (f_s)": (-1, 2),
            "Sourcé": (0, 2),
            "Messaged": (1, 2),
            "AKLIFé": (2, 2),
            "KLIF": (3, 2),
            "RDV1": (4, 2),
            "RDV2": (5, 2),
            "Proposal": (6, 2),
            "Consultants": (7, 2),
            "Non retenu": (0, 1),
            "Pas de retour": (1, 1),
            "Rejeté": (1, 0),
            "AKLIF négatif": (2, 1),
            "RDV1 rejeté": (3, 1),
            "RDV2 négatif": (4, 1),
            "RDV3 négatif": (5, 1),
            "Proposition rejetée": (6, 1),
        }

        plt.figure(figsize=(16, 8))
        nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=3500, font_size=10, font_weight="bold", edge_color="gray", arrowsize=20, connectionstyle="arc3,rad=0.1")

        # Add edge labels (process rates)
        edge_labels = {(u, v): label for u, v, label in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        plt.title("Causal Loop Diagram of Recruitment Process (with Sourcing f_s)")
        plt.show()

if __name__ == "__main__":
    model = RecruitmentModel(0.1, 0.9, 0.8, 0.1, 0.1, 0.2, 0.8, 0.6, 0.4, 0.1, 0.9, 0.5, 0.5, 0.2, 0.8)
    solution = model.run_simulation()
    model.plot_results(solution)
    model.plot_causal_loop_diagram()
