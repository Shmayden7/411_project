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
    def __init__(self, cities_data, n, cities=None):
        # Convert cities_data to a list of dictionaries if it isn't already
        cities_list = list(cities_data.to_dict(orient="records"))

        if cities:
            # Initialize with specified cities
            self.nodes = [city for city in cities_list if city['city'] in cities]
            if len(self.nodes) < len(cities):
                raise ValueError("Some specified cities were not found in the data.")
        else:
            # Initialize with random cities if no specific cities are provided
            self.nodes = random.sample(cities_list, n)

        self.edges = self._create_edges()
        self._remove_looping_edges()

    def _create_edges(self):
        edges = []
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                city1, city2 = self.nodes[i], self.nodes[j]
                dist = self.haversine_distance(city1['lat'], city1['lng'], city2['lat'], city2['lng'])
                edges.append((city1['city'], city2['city'], dist))
        return edges

    def _remove_looping_edges(self):
        # Remove any edges that loop back to the same city
        self.edges = [edge for edge in self.edges if edge[0] != edge[1]]

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in kilometers
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        return distance
    
    def haversine_heuristic(self, u, v):
        # Heuristic function for A* algorithm, calculating Haversine distance between two cities
        city1 = self.get_city_data(u)
        city2 = self.get_city_data(v)
        if city1 is None or city2 is None:
            raise ValueError("One or both of the specified cities were not found in the graph.")
        return self.haversine_distance(city1['lat'], city1['lng'], city2['lat'], city2['lng'])
    
    def get_city_data(self, city_name):
        for city in self.nodes:
            if city['city'] == city_name:
                return city
        return None  # Or raise an exception if the city is not found
    
    def remove_edge(self, city1_name, city2_name):
        # Removes the link (edge) between two cities, if it exists.

        # Convert the edge list to a list of tuples for easier manipulation
        edges_as_tuples = [(edge[0], edge[1]) for edge in self.edges]

        # Check if the edge exists in either direction
        if (city1_name, city2_name) in edges_as_tuples or (city2_name, city1_name) in edges_as_tuples:
            # Remove the edge by filtering it out
            self.edges = [edge for edge in self.edges if edge[0] != city1_name or edge[1] != city2_name]
            self.edges = [edge for edge in self.edges if edge[0] != city2_name or edge[1] != city1_name]
            print(f"Link between {city1_name} and {city2_name} removed.")
        else:
            print(f"No direct link found between {city1_name} and {city2_name}.")

    def to_networkx_graph(self):
        G = nx.Graph()
        for city in self.nodes:
            # Ensure that the 'city' dictionary has 'lng' and 'lat' keys
            # Add city as a node along with the latitude and longitude attributes
            G.add_node(city['city'], lng=city['lng'], lat=city['lat'])
        for edge in self.edges:
            # Assuming each edge is a tuple (city1, city2, distance)
            G.add_edge(edge[0], edge[1], weight=edge[2])
        return G

    def get_neighbors(self, city_name):
        return [edge[1] for edge in self.edges if edge[0] == city_name] + \
               [edge[0] for edge in self.edges if edge[1] == city_name]
    
    def get_edge_weight(self, city1_name, city2_name):
        """
        Get the weight of the edge between two cities.
        """
        for edge in self.edges:
            if (edge[0] == city1_name and edge[1] == city2_name) or \
               (edge[1] == city1_name and edge[0] == city2_name):
                return edge[2]  # Assuming edge is a tuple (city1, city2, weight)
        return None  # Return None or raise an exception if the edge is not found
    
    def select_random_cities(self):
        if len(self.nodes) < 2:
            raise ValueError("The graph needs at least two cities to select a start and end.")

        start_city, end_city = random.sample(self.nodes, 2)
        return start_city['city'], end_city['city']
    
    def print_graph(self):
        for edge in self.edges:
            print(f"Distance between {edge[0]} and {edge[1]}: {edge[2]:.2f} km") 

    def visualize_graph(self, title, start_city=None, end_city=None):
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

        # Define node colors: start city green, end city red, others lightblue
        node_colors = []
        for node in G.nodes():  # Iterate over nodes in the graph
            if node == start_city:
                node_colors.append('green')
            elif node == end_city:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')

        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                edge_color='gray', node_size=500, font_size=8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

        plt.title(title or "City Graph")
        
        # Use plt.annotate for the title
        plt.annotate(title or "City Graph with Shortest Path", xy=(0, 1), xycoords='axes fraction',
                    xytext=(10, -10), textcoords='offset points',
                    ha='left', va='top', fontsize=14, color='black',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black'))


        if title:
            plt.savefig(f'{title}.png', format='png')
        plt.show()

    def visualize_shortest_path(self, path, title):
        G = nx.Graph()
        pos = {}
        total_distance = 0

        # Add nodes with position (latitude, longitude)
        for node in self.nodes:
            G.add_node(node['city'])
            pos[node['city']] = (node['lng'], node['lat'])

        # Add only the existing edges from the graph structure to be displayed in grey
        for edge in self.edges:
            G.add_edge(edge[0], edge[1], weight=edge[2])

        # Draw the graph with grey edges
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                edge_color='gray', node_size=500, font_size=8)

        # Filter the path edges to include only those that exist in the graph structure
        path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1) if G.has_edge(path[i], path[i+1])]

        # Calculate the total distance of the path
        for i in range(len(path) - 1):
            if G.has_edge(path[i], path[i+1]):
                edge_data = G.get_edge_data(path[i], path[i+1])
                total_distance += edge_data['weight']

        # Highlight the shortest path
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        # Color nodes in the path
        start_node = [path[0]]
        end_node = [path[-1]]
        middle_nodes = path[1:-1]
        nx.draw_networkx_nodes(G, pos, nodelist=start_node, node_color='green')
        nx.draw_networkx_nodes(G, pos, nodelist=end_node, node_color='red')
        nx.draw_networkx_nodes(G, pos, nodelist=middle_nodes, node_color='orange')

        # Use plt.annotate for the title
        plt.annotate(title or "City Graph with Shortest Path", xy=(0, 1), xycoords='axes fraction',
                    xytext=(10, -10), textcoords='offset points',
                    ha='left', va='top', fontsize=14, color='black',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black'))

        # Annotation for the total distance
        plt.annotate(f'Total Distance: \n{total_distance:.2f} km', xy=(0, 1), xycoords='axes fraction',
                    xytext=(10, -35), textcoords='offset points',
                    ha='left', va='top', fontsize=12, color='black',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black'))

        # Save the figure if a title is provided
        if title:
            plt.savefig(f'{title}.png', format='png')
        plt.show()