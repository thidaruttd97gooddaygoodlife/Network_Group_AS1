import asyncio

class Node:
    def __init__(self, name):
        self.name = name
        self.distances = {}
        self.neighbors = {}
        self.queue = asyncio.Queue()

    async def initialize_distances(self, graph_size):
        self.distances = {i: float('inf') for i in range(graph_size)}
        self.distances[self.name] = 0

    async def add_neighbor(self, neighbor, weight):
        self.neighbors[neighbor] = weight

    async def send_message(self, target_node, distance):
        await target_node.queue.put((self.name, distance))

    async def process_messages(self, distances_over_time, iteration):
        updated = False
        while not self.queue.empty():
            sender, distance = await self.queue.get()
            if distance < self.distances[sender]:
                self.distances[sender] = distance
                updated = True
                for neighbor, weight in self.neighbors.items():
                    await self.send_message(neighbor, distance + weight)
        if updated:
            distances_over_time[self.name].append(self.distances.copy())
