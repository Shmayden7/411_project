from classes import MazeCanvas
from constants import example_mazes
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

################## Constants
rows = 10
cols = 10
obstacle_density = 0.3  # Adjust this value to control obstacle density
master = tk.Tk()

start = (0,0)
goal = (9,9)
##################

maze_instance = MazeCanvas(master=master, maze=example_mazes[0], start=start, goal=goal)

##Custom built A* method##
solved_maze = maze_instance.a_star()
maze_instance.draw_maze(solved_maze) #Draw the maze GUI

##Netwokx A*##
G = maze_instance.to_networkx_graph()

# Remove nodes from nx graph based on the maze map
nodes_to_remove = [(i, j) for i in range(len(maze_instance.maze)) for j in range(len(maze_instance.maze[0])) if maze_instance.maze[i][j] == 1]
G.remove_nodes_from(nodes_to_remove)

pos = {node: (node[1], -node[0]) for node in G.nodes()}  # Adjusting positions for better visualization
package_opt_path = nx.astar_path(G, start, goal, heuristic=maze_instance.heuristic, weight='weight')

# Specify node color to show shortest path
node_colors = ['red' if node in package_opt_path else 'blue' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=100, node_color=node_colors)
plt.show()
print(package_opt_path)

##Floyd-Warshall##
floyd_warshall_opt_path = shortest_path_floyd_warshall(G, start_city, end_city)
print(floyd_warshall_opt_path)




