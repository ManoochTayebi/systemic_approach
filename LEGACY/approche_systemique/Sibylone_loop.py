import matplotlib.pyplot as plt
import networkx as nx

class RecruitmentModel:
    def __init__(self):
        self.sourcing_rate = 60
        self.retention_rate = 0.1
        self.messaging_rate = 0.9
        self.response_rate = 0.8
        self.rejection_rate = 0.1
        self.aklife_rate = 0.1

class InterContratModel:
    def __init__(self):
        self.initial_consultants = 17
        self.retour_mission_rate = 1/140
        self.departure_rate = 0.05

class CommerceModel:
    def __init__(self):
        self.stock_ao_rate = 13
        self.opportunites_rate = 2.5
        self.candidats_positionnes_rate = 0.3
        self.presentation_clients_rate = 0.33

class PlotCausalLoop:
    def plot_causal_loop_diagram(self, recruitment_model, inter_contrat_model, commerce_model):
        G = nx.DiGraph()

        # Define nodes by department
        recruitment_nodes = [
            "Sourcing", "Messaging", "AKLIFé", "KLIF", "First Interview (RDV1)", 
            "Second Interview (RDV2)", "Proposal Sent"
        ]
        inter_contrat_nodes = ["Consultant in INTER-CONTRAT", "Consultant in MISSION"]
        commerce_nodes = ["Stock AO", "Opportunités", "Candidats positionnés", "Presentation clients", "Départ en mission"]

        other_nodes = [
            "Not Retained", "Not Responded", "Rejected", "Failed KLIF", "Rejected at KLIF", 
            "Rejected at RDV1", "Rejected at RDV2", "Rejected Proposal", "Not Selected", "Opportunités perdues", 
            "Ignored", "Rejected"
        ]

        # Add all nodes
        G.add_nodes_from(recruitment_nodes + inter_contrat_nodes + commerce_nodes + other_nodes)

        # Define edges
        edges = [
            ("Sourcing", "Messaging"), ("Sourcing", "Not Retained"),
            ("Messaging", "Not Responded"), ("Messaging", "Rejected"), ("Messaging", "AKLIFé"),
            ("AKLIFé", "Failed KLIF"), ("AKLIFé", "KLIF"),
            ("KLIF", "Rejected at KLIF"), ("KLIF", "First Interview (RDV1)"),
            ("First Interview (RDV1)", "Rejected at RDV1"), ("First Interview (RDV1)", "Second Interview (RDV2)"),
            ("Second Interview (RDV2)", "Rejected at RDV2"), ("Second Interview (RDV2)", "Proposal Sent"),
            ("Proposal Sent", "Rejected Proposal"), ("Proposal Sent", "Consultant in INTER-CONTRAT"),
            ("Stock AO", "Opportunités"), ("Stock AO", "Not Selected"),
            ("Opportunités", "Candidats positionnés"), ("Opportunités", "Opportunités perdues"),
            ("Candidats positionnés", "Presentation clients"), ("Candidats positionnés", "Ignored"),
            ("Presentation clients", "Départ en mission"), ("Presentation clients", "Rejected"),
            ("Consultant in INTER-CONTRAT", "Consultant in MISSION"), ("Consultant in MISSION", "Consultant in INTER-CONTRAT")
        ]
        G.add_edges_from(edges)

        # Define edge labels
        edge_labels = {
            ("Sourcing", "Messaging"): "0.9", 
            ("Sourcing", "Not Retained"): "0.1",
            ("Messaging", "Not Responded"): "0.8", 
            ("Messaging", "Rejected"): "0.1", 
            ("Messaging", "AKLIFé"): "0.1",
            ("Stock AO", "Opportunités"): "10/13", 
            ("Stock AO", "Not Selected"): "3/13",
            ("Opportunités", "Candidats positionnés"): "0.3", 
            ("Opportunités", "Opportunités perdues"): "0.7",
            ("Candidats positionnés", "Presentation clients"): "0.33", 
            ("Candidats positionnés", "Ignored"): "0.67"
        }

        # Custom positions to align nodes by department
        pos = {
            # Recruitment
            "Sourcing": (0, 3), "Messaging": (1, 3), "AKLIFé": (2, 3), "KLIF": (3, 3),
            "First Interview (RDV1)": (4, 3), "Second Interview (RDV2)": (5, 3), "Proposal Sent": (6, 3),
            
            # Inter-Contrat
            "Consultant in INTER-CONTRAT": (7, 2), "Consultant in MISSION": (8, 2),

            # Commerce
            "Stock AO": (0, 1), "Opportunités": (1, 1), "Candidats positionnés": (2, 1),
            "Presentation clients": (3, 1), "Départ en mission": (4, 1),
            
            # Other Nodes (Failures/Rejections)
            "Not Retained": (1, 4), "Not Responded": (2, 4), "Rejected": (3, 4), "Failed KLIF": (4, 4),
            "Rejected at KLIF": (5, 4), "Rejected at RDV1": (6, 4), "Rejected at RDV2": (7, 4), 
            "Rejected Proposal": (8, 4), "Not Selected": (2, 0), "Opportunités perdues": (3, 0),
            "Ignored": (4, 0), "Rejected": (5, 0)
        }

        plt.figure(figsize=(12, 6))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, nodelist=recruitment_nodes, node_color='lightblue', node_size=1200)
        nx.draw_networkx_nodes(G, pos, nodelist=inter_contrat_nodes, node_color='lightgreen', node_size=1200)
        nx.draw_networkx_nodes(G, pos, nodelist=commerce_nodes, node_color='lightcoral', node_size=1200)
        nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, node_color='gray', node_size=800)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='black', width=1.5, arrowsize=15)

        # Draw edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

        plt.title("Causal Loop Diagram - Recruitment, Inter-Contrat, and Commerce")
        plt.show()

# Create models
recruitment_model = RecruitmentModel()
inter_contrat_model = InterContratModel()
commerce_model = CommerceModel()

# Plot causal loop diagram
plotter = PlotCausalLoop()
plotter.plot_causal_loop_diagram(recruitment_model, inter_contrat_model, commerce_model)
