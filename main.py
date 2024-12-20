import asyncio
from graph import Graph
from distributed_bellman_ford import DistributedBellmanFord
from visualization import Visualization
import networkx as nx

if __name__ == "__main__":
    graph = Graph()
    graph.add_edge(0, 1, 4)
    graph.add_edge(0, 2, 2)
    graph.add_edge(1, 2, 3)
    graph.add_edge(1, 3, 2)
    graph.add_edge(2, 3, 4)
    graph.add_edge(3, 4, 2)
    graph.add_edge(4, 5, 1)
    graph.add_edge(5, 0, 1)  # No Negative weight edge

    dbf = DistributedBellmanFord(graph)
    dbf.create_nodes()
    asyncio.run(dbf.run(iterations=len(graph.adj_list)))

    is_negative_cycle, distances, predecessors = graph.detect_negative_cycle()
    pos = nx.spring_layout(nx.DiGraph(graph.adj_list))
    if is_negative_cycle:
        print("Negative cycle detected!")
        Visualization(graph, dbf.distances_over_time).highlight_cycle_or_negative(predecessors, pos, 'red')
    else:
        print("No negative cycle detected.")
        Visualization(graph, dbf.distances_over_time).highlight_cycle_or_negative(predecessors, pos, 'green')

    vis = Visualization(graph, dbf.distances_over_time)
    vis.draw_graph()
    vis.plot_distances()
