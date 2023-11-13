import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import heapq

def a_star_cities(graph, max_visits, min_visits, start_city, end_city):
    def heuristic(city_name1, city_name2):
        return graph.haversine_distance(city_name1, city_name2)

    open_set = []
    heapq.heappush(open_set, (0, start_city, [start_city], 0)) # (cost, current_city, path, visits)

    while open_set:
        _, current_city, path, visits = heapq.heappop(open_set)

        if current_city == end_city and min_visits <= visits <= max_visits:
            return path

        if visits > max_visits:
            continue

        for neighbor in graph.get_neighbors(current_city):
            if neighbor not in path:
                new_path = path + [neighbor]
                new_visits = visits + 1
                estimated_cost = visits + heuristic(current_city, end_city)
                heapq.heappush(open_set, (estimated_cost, neighbor, new_path, new_visits))

    return None  # No path found  


