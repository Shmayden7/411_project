from deap import base, creator, tools, algorithms
import networkx as nx
import random

def shortest_path_floyd_warshall(G, start_city, end_city):
    # Run Floyd-Warshall algorithm
    pred, _ = nx.floyd_warshall_predecessor_and_distance(G, weight='weight')

    # Reconstruct the shortest path
    path = []
    try:
        current = end_city
        while current != start_city:
            path.append(current)
            current = pred[start_city][current]
        path.append(start_city)
        path.reverse()
    except KeyError:
        # No path found
        path = []

    return path