import asyncio
from node import Node
from graph import Graph
import os
print("Current working directory:", os.getcwd())

class DistributedBellmanFord:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = {}
        self.distances_over_time = {}

    def create_nodes(self):
        # Create nodes from graph and establish neighbors
        for u, neighbors in self.graph.adj_list.items():
            if u not in self.nodes:
                self.nodes[u] = Node(u)
            for v, weight in neighbors:
                if v not in self.nodes:
                    self.nodes[v] = Node(v)
                asyncio.run(self.nodes[u].add_neighbor(self.nodes[v], weight))

    async def initialize(self):
        # Initialize distances
        tasks = []
        for node in self.nodes.values():
            self.distances_over_time[node.name] = []
            tasks.append(node.initialize_distances(len(self.nodes)))
        await asyncio.gather(*tasks)

    async def run(self, iterations):
        await self.initialize()

        for i in range(iterations):
            print(f"\nIteration {i}:")
            tasks = [node.process_messages(self.distances_over_time, i) for node in self.nodes.values()]
            await asyncio.gather(*tasks)
            self.print_iteration_distances(i)

        self.print_final_distances()

    def print_iteration_distances(self, iteration):
        print(f"\nIteration {iteration}:")
        for node, distances in self.distances_over_time.items():
            if distances:
                print(f"Node {node}: {distances[-1]}")
            else:
                print(f"Node {node}: No distances recorded yet")

    def print_final_distances(self):
        print("\nFinal Distances:")
        for node, distances in self.distances_over_time.items():
            print(f"Node {node}: {distances[-1] if distances else 'No distances recorded'}")

if __name__ == "__main__":
    # ตัวอย่าง
    print(f"Current working directory: {os.getcwd()}")
    # หรือเรียกฟังก์ชันหลักที่คุณสร้างขึ้น
