import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import networkx as nx
import random
import math

class City:
    def __init__(self, city, city_ascii, state_id, state_name, county_fips, county_name, 
                 latitude, longitude, population, density):
        self.city = city
        self.city_ascii = city_ascii
        self.state_id = state_id
        self.state_name = state_name
        self.county_fips = county_fips
        self.county_name = county_name
        self.latitude = latitude
        self.longitude = longitude
        self.population = population
        self.density = density

    @classmethod
    def from_city_name(cls, cities_data, city_name):
        city_data = cities_data[cities_data['city'] == city_name].iloc[0]
        return cls(city_data['city'], city_data['city_ascii'], city_data['state_id'], 
                   city_data['state_name'], city_data['county_fips'], city_data['county_name'], 
                   city_data['lat'], city_data['lng'], city_data['population'], city_data['density'])
    
class CityGraph:
    def __init__(self, cities_data, n):
        self.nodes = random.sample(list(cities_data.to_dict(orient="records")), n)
        self.edges = self._create_edges()

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in kilometers
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        return distance

    def _create_edges(self):
        edges = []
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                city1, city2 = self.nodes[i], self.nodes[j]
                dist = self._haversine_distance(city1['lat'], city1['lng'], city2['lat'], city2['lng'])
                edges.append((city1['city'], city2['city'], dist))
        return edges
    
    def get_neighbors(self, city_name):
        return [edge[1] for edge in self.edges if edge[0] == city_name] + \
               [edge[0] for edge in self.edges if edge[1] == city_name]
    
    def select_random_cities(self):
        if len(self.nodes) < 2:
            raise ValueError("The graph needs at least two cities to select a start and end.")

        start_city, end_city = random.sample(self.nodes, 2)
        return start_city['city'], end_city['city']
    
    def print_graph(self):
        for edge in self.edges:
            print(f"Distance between {edge[0]} and {edge[1]}: {edge[2]:.2f} km") 

    def visualize_graph(self):
        G = nx.Graph()
        pos = {}
        edge_labels = {}

        # Add nodes with position (latitude, longitude)
        for node in self.nodes:
            G.add_node(node['city'])
            pos[node['city']] = (node['lng'], node['lat'])

        # Add edges with distance as weight and prepare edge labels
        for edge in self.edges:
            G.add_edge(edge[0], edge[1], weight=edge[2])
            edge_labels[(edge[0], edge[1])] = f"{edge[2]:.2f} km"

        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                edge_color='gray', node_size=500, font_size=8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

        plt.title("City Graph")
        plt.show()