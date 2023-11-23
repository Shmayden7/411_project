import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import heapq
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles
    return c * r

def heuristic(city_graph, city1_name, city2_name):
    """
    Heuristic function for A* algorithm, calculating Haversine distance between two cities.
    """
    city1_data = city_graph.get_city_data(city1_name)
    city2_data = city_graph.get_city_data(city2_name)
    
    if city1_data is None or city2_data is None:
        raise ValueError("One or both of the specified cities were not found in the graph.")
    
    return haversine_distance(city1_data['lat'], city1_data['lng'], city2_data['lat'], city2_data['lng'])

def a_star_cities(graph, max_visits, start_city, end_city):

    open_set = []
    heapq.heappush(open_set, (0, start_city, [start_city], 0))  # (estimated_total_cost, current_city, path, accumulated_cost)

    while open_set:
        _, current_city, path, accumulated_cost = heapq.heappop(open_set)

        if current_city == end_city:
            return path

        if len(path) - 1 > max_visits:  # minus 1 because path includes start_city
            continue

        for neighbor in graph.get_neighbors(current_city):
            if neighbor not in path:
                new_path = path + [neighbor]
                # Accumulate actual cost so far
                edge_weight = graph.get_edge_weight(current_city, neighbor)
                new_accumulated_cost = accumulated_cost + edge_weight
                # Estimated total cost is actual cost so far plus heuristic estimate to goal
                estimated_total_cost = new_accumulated_cost + heuristic(graph, neighbor, end_city)
                heapq.heappush(open_set, (estimated_total_cost, neighbor, new_path, new_accumulated_cost))

    return None  # No path found