import networkx as nx
import matplotlib.pyplot as plt
from SibyloneModel import SibyloneModel

class PlotCausalLoop:
    def __init__(self):
        self.model = SibyloneModel()
        self.G = nx.DiGraph()

    def plot_causal_loop_diagram(self):
        # Extract parameters as nodes from the model
        nodes = list(self.model.parameters.keys())
        self.G.add_nodes_from(nodes)

        # Extract equations as edges from the model
        for equation in self.model.equations:
            variables = equation['variables']
            for i in range(len(variables)):
                for j in range(i + 1, len(variables)):
                    if variables[i] != variables[j]:
                        self.G.add_edge(variables[i], variables[j])

        # Group nodes into three distinct departments
        department1_nodes = [node for node in nodes if node.startswith('dept1')]
        department2_nodes = [node for node in nodes if node.startswith('dept2')]
        department3_nodes = [node for node in nodes if node.startswith('dept3')]

        # Define a dictionary pos where nodes within the same department are positioned together
        pos = {}
        for i, node in enumerate(department1_nodes):
            pos[node] = (0, -i)
        for i, node in enumerate(department2_nodes):
            pos[node] = (1, -i)
        for i, node in enumerate(department3_nodes):
            pos[node] = (2, -i)

        # Draw the directed graph
        nx.draw(self.G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=12)
        plt.show()


if __name__ == "__main__":
    plot_causal_loop = PlotCausalLoop()
    plot_causal_loop.plot_causal_loop_diagram()