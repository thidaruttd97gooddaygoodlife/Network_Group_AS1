from collections import defaultdict


class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)

    def add_edge(self, u, v, weight):
        self.adj_list[u].append((v, weight))

    def detect_negative_cycle(self):
        nodes = list(self.adj_list.keys())
        distances = {node: float('inf') for node in nodes}
        distances[0] = 0
        predecessors = {node: None for node in nodes}
        
        # Bellman-Ford algorithm
        for _ in range(len(nodes) - 1):
            for u in nodes:
                for v, weight in self.adj_list[u]:
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        predecessors[v] = u

        # Check for negative cycles
        for u in nodes:
            for v, weight in self.adj_list[u]:
                if distances[u] + weight < distances[v]:
                    print(f"Negative cycle detected via edge {u} -> {v} with weight {weight}")
                    return True, distances, predecessors

        return False, distances, predecessors
