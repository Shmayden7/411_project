from classes import MazeCanvas
from constants import example_mazes
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import time

################## Constants
master = tk.Tk()

start = (0, 0)
goal = (9, 9)
##################

maze_instance = MazeCanvas(master=master, maze=example_mazes[0], start=start, goal=goal)

################## Custom built A* method 
start_time_1 = time.time()
solved_maze = maze_instance.a_star()
runtime_custom_a_star = (time.time() - start_time_1)*1000
print(f'Custom Built A* Runtime: {runtime_custom_a_star}')
maze_instance.draw_maze(solved_maze)  # Draw the maze GUI
################## 

################## NetworkX A*
G = maze_instance.to_networkx_graph()

# Remove nodes from nx graph based on the maze map
nodes_to_remove = [(i, j) for i in range(len(maze_instance.maze)) for j in range(len(maze_instance.maze[0])) if maze_instance.maze[i][j] == 1]
G.remove_nodes_from(nodes_to_remove)

pos = {node: (node[1], -node[0]) for node in G.nodes()}  

start_time_2 = time.time()
package_opt_path = nx.astar_path(G, start, goal, heuristic=maze_instance.heuristic, weight='weight')
runtime_networkx_a_star = (time.time() - start_time_2)*1000
print(f'NetworkX A* Runtime: {runtime_networkx_a_star}')

# Visualization - A* shortest path
node_colors = ['red' if node in package_opt_path else 'blue' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=100, node_color=node_colors)
plt.title("A* Shortest Path")
plt.show()
print(f"A* Shortest Path: {package_opt_path}")
##################


################## NetworkX Dijkstras ##
start_time_3 = time.time()
dijkstra_opt_path = nx.shortest_path(G, source=start, target=goal, weight='weight')
runtime_dijkstras = (time.time() - start_time_3)*1000
print(f'Dijkstras Runtime: {runtime_dijkstras}')

# Visualization - Dijkstras shortest path
dijkstra_node_colors = ['green' if node in dijkstra_opt_path else 'blue' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=100, node_color=dijkstra_node_colors)
plt.title("Dijkstra's Shortest Path")
plt.show()

print(f"Dijkstra's Shortest Path: {dijkstra_opt_path}")
##################