import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from algrothims import a_star_cities
from classes import CityGraph
from constants import testing_cities_start_end, testing_cities_total

################## Constants
cities_data = pd.read_csv('uscities.csv')
cities_in_graph = len(testing_cities_total[0])
graph_title = 'graph'
graph_solved_title = 'graph_solved'
##################

################## Running Code
# 
for i, subset in enumerate(testing_cities_total):

    ### Defining Starting and Ending City
    # start_city, end_city = city_graph.select_random_cities()
    start_city = testing_cities_start_end[i][0]
    end_city = testing_cities_start_end[i][1]

    # Intilizing Graph Instance & Visualizing
    city_graph = CityGraph(cities_data, cities_in_graph, subset)

    ### Remove the link between start city and end city so that 
    ### A* can find the shortest path which is not the direct rout
    print(f"Edges before removal: {len(city_graph.edges)}")
    city_graph.remove_link(start_city, end_city)
    print(f"Edges after removal: {len(city_graph.edges)}")

    # Convert to a networkx graph
    G = city_graph.to_networkx_graph()   
    # # Position the nodes using one of the layout algorithms. For geographical graphs, you might use the latitude and longitude.
    # pos = {city: (data['lng'], data['lat']) for city, data in G.nodes(data=True)}
    # # Draw the nodes and edges
    # nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', edge_color='gray')
    # # If you have edge labels (like distances), you can draw them too.
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # # Show the plot
    # plt.show()

    ### Plot the graph structure without annotations or algrothims    
    city_graph.visualize_graph(title=f'{i}_'+graph_title, start_city=start_city, end_city=end_city)

    ### Predictions
    # Making Predictions using the custom built A*
    path_custom_a_star = a_star_cities(city_graph, max_visits=cities_in_graph, start_city=start_city, end_city=end_city)
    print(f'path_custom_a_star: {path_custom_a_star}')
    # Making predictions using the NX package A*
    path_networkx_a_star = nx.astar_path(G, start_city, end_city, heuristic=city_graph.haversine_heuristic, weight='weight')
    print(f'path_networkx_a_star {path_networkx_a_star}')
    ###

    ### Visulizing Predictions
    city_graph.visualize_shortest_path(path=path_custom_a_star, title=f'{i}_custom_A*_'+graph_solved_title)
    city_graph.visualize_shortest_path(path=path_networkx_a_star, title=f'{i}_networkx_A*_'+graph_solved_title)
    ###
##################

