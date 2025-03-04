################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import matplotlib.pyplot as plt
import networkx as nx
from example_equations_class import RecruitmentModel

class PlotCausalLoop:
    def plot_causal_loop_diagram(self, model):
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
            ("Sourcé", "Messaged", f"r_m = {model.r_m}"),  
            ("Sourcé", "Non retenu", f"r_s = {model.r_s}"),  
            ("Messaged", "Pas de retour", f"r_nr = {model.r_nr}"),  
            ("Messaged", "Rejeté", f"r_ref = {model.r_ref}"),  
            ("Messaged", "AKLIFé", f"r_ak = {model.r_ak}"),  
            ("AKLIFé", "AKLIF négatif", f"r_akneg = {model.r_akneg}"),  
            ("AKLIFé", "KLIF", f"r_k = {model.r_k}"),  
            ("KLIF", "RDV1", f"r_r1 = {model.r_r1}"),  
            ("KLIF", "RDV1 rejeté", f"r_kneg = {model.r_kneg}"),  
            ("RDV1", "RDV2", f"r_r2 = {model.r_r2}"),  
            ("RDV1", "RDV2 négatif", f"r_r2neg = {model.r_r2neg}"),  
            ("RDV2", "Proposal", f"r_p = {model.r_p}"),  
            ("RDV2", "RDV3 négatif", f"r_r3neg = {model.r_r3neg}"),  
            ("Proposal", "Consultants", f"r_c = {model.r_c}"),  
            ("Proposal", "Proposition rejetée", f"r_pref = {model.r_pref}")
        ]

        G.add_edges_from([(u, v) for u, v, _ in edges])

        # Define layout (aligned positioning)
        pos = {
            "Sourcing (f_s)": (-1, 2), "Sourcé": (0, 2), "Messaged": (1, 2), "AKLIFé": (2, 2), "KLIF": (3, 2), "RDV1": (4, 2), 
            "RDV2": (5, 2), "Proposal": (6, 2), "Consultants": (7, 2), "Non retenu": (0, 1), "Pas de retour": (1, 1), "Rejeté": (1, 0), 
            "AKLIF négatif": (2, 1), "RDV1 rejeté": (3, 1), "RDV2 négatif": (4, 1), "RDV3 négatif": (5, 1), "Proposition rejetée": (6, 1)
        }

        plt.figure(figsize=(16, 8))
        nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=3500, font_size=10, font_weight="bold", edge_color="gray", arrowsize=20, connectionstyle="arc3,rad=0.1")

        # Add edge labels (process rates)
        edge_labels = {(u, v): label for u, v, label in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        plt.title("Causal Loop Diagram of Recruitment Process (with Sourcing f_s)")
        plt.show()

if __name__ == "__main__":
    model = RecruitmentModel()
    plotter = PlotCausalLoop()
    plotter.plot_causal_loop_diagram(model)