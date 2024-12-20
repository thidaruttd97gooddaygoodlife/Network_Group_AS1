import networkx as nx
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, graph, distances_over_time):
        self.graph = graph
        self.distances_over_time = distances_over_time

    def highlight_cycle_or_negative(self, predecessors, pos, color):
        G = nx.DiGraph(self.graph.adj_list)
        for node in predecessors:
            cycle_path = []
            current = node
            while current is not None:
                cycle_path.append(current)
                current = predecessors.get(current)
                if current in cycle_path:  # Cycle detected
                    cycle_path = cycle_path[cycle_path.index(current):]
                    break
            if len(cycle_path) > 1:  # Valid cycle found
                edges = [(cycle_path[i], cycle_path[i + 1]) for i in range(len(cycle_path) - 1)]
                nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=3, alpha=0.5)
        plt.show()

    def draw_graph(self):
        G = nx.DiGraph(self.graph.adj_list)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10, font_weight='bold')
        plt.show()

    def plot_distances(self):
        for node, distances in self.distances_over_time.items():
            plt.plot(range(len(distances)), [d[node] for d in distances], label=f"Node {node}")
        plt.xlabel("Iteration")
        plt.ylabel("Distance")
        plt.title("Distance Convergence")
        plt.legend()
        plt.show()
