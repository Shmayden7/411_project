import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from algrothims import a_star_cities
from classes import CityGraph
from constants import testing_cities_start_end, testing_cities_total, path_deletion

################## Constants
cities_data = pd.read_csv('uscities.csv')
cities_in_graph = len(testing_cities_total[0])
graph_title = 'graph'
graph_solved_title = 'solved'
##################

def estimate_visualize_path(city_graph, G, start_city, end_city, plot, iter):
    if plot == 0:
        plot_name = 'A'
    elif plot == 1:
        plot_name = 'B'

    ### Plot the graph structure without annotations or algrothims    
    city_graph.visualize_graph(title=f'{plot_name}_'+graph_title, start_city=start_city, end_city=end_city)

    ### Predictions
    # Making Predictions using the custom built A*
    path_custom_a_star = a_star_cities(city_graph, max_visits=cities_in_graph, start_city=start_city, end_city=end_city)
    print(f'path_custom_a_star: {path_custom_a_star}')
    # Making predictions using the NX package A*
    path_networkx_a_star = nx.astar_path(G, start_city, end_city, heuristic=city_graph.haversine_heuristic, weight='weight')
    print(f'path_networkx_a_star {path_networkx_a_star}')
    # Making predictions using the NX package Dijkstra Algrothim
    path_networkx_dijkstra = nx.dijkstra_path(G, source=start_city, target=end_city, weight='weight')
    print(f'path_networkx_dijkstra {path_networkx_dijkstra}\n')
    ###

    ### Visulizing Predictions
    city_graph.visualize_shortest_path(path=path_custom_a_star, title=f'Plot:{plot_name}_iter:{iter}_custom_A*_'+graph_solved_title)
    city_graph.visualize_shortest_path(path=path_networkx_a_star, title=f'Plot:{plot_name}_iter:{iter}_networkx_A*_'+graph_solved_title)
    city_graph.visualize_shortest_path(path=path_networkx_dijkstra, title=f'Plot{plot_name}_iter:{iter}_networkx_dijkstra_'+graph_solved_title)
    ###


################## Running Code

for i, subset in enumerate(testing_cities_total):

    ### Defining Starting and Ending City
    # start_city, end_city = city_graph.select_random_cities()
    start_city = testing_cities_start_end[i][0]
    end_city = testing_cities_start_end[i][1]

    # Intilizing Graph Instance & Visualizing
    city_graph = CityGraph(cities_data, cities_in_graph, subset)
    G = city_graph.to_networkx_graph() 

    for j, deletion_pair in enumerate(path_deletion[i]):

        # Edges to remove
        e1 = deletion_pair[0]
        e2 = deletion_pair[1]

        ### Remove the link between start city and end city so that 
        ### A* can find the shortest path which is not the direct rout
        city_graph.remove_edge(e1, e2)
        G.remove_edge(e1,e2)

        estimate_visualize_path(city_graph=city_graph, G=G, start_city=start_city, end_city=end_city, plot=i, iter=j)

##################