import pandas as pd

from algrothims import a_star_cities
from classes import City, CityGraph

################## Constants
cities_data = pd.read_csv('uscities.csv')
cities_in_graph = 9
min_visits = 3
##################

################## Running Code
city_graph = CityGraph(cities_data, cities_in_graph)
city_graph.visualize_graph()

start_city, end_city = city_graph.select_random_cities()
print(start_city)
print(end_city)

path = a_star_cities(city_graph, max_visits=cities_in_graph, min_visits=min_visits, start_city=start_city, end_city=end_city)
print(path)
##################

