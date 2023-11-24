import heapq
import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt

class MazeNode:
    def __init__(self, position, parent=None, cost=0, heuristic=0):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

class MazeCanvas:
    def __init__(self, master, maze, start, goal):
        self.master = master
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = start
        self.goal = goal
        self.canvas = tk.Canvas(master, width=self.cols * 30, height=self.rows * 30)
        self.canvas.pack()

    def heuristic(self, current, goal):
        # Manhattan distance heuristic
        dist = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        return dist
    
    def get_neighbors(self, node):
        neighbors = []
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for move in moves:
            new_position = (node.position[0] + move[0], node.position[1] + move[1])

            if 0 <= new_position[0] < self.rows and 0 <= new_position[1] < self.cols and self.maze[new_position[0]][new_position[1]] == 0:
                neighbors.append(MazeNode(new_position, parent=node))

        return neighbors

    def to_networkx_graph(self):
        G = nx.Graph()

        for i in range(self.rows):
            for j in range(self.cols):
                current_position = (i, j)
                current_node = MazeNode(current_position)

                # Add the current node to the graph
                G.add_node(current_position)

                # Get neighbors for the current node
                neighbors = self.get_neighbors(current_node)
                
                # Connect the current node to its neighbors
                for neighbor in neighbors:
                    G.add_edge(current_position, neighbor.position)

        return G
    
    def a_star(self):
        start_node = MazeNode(self.start)
        start_node.heuristic = self.heuristic(self.start, self.goal)

        open_set = [start_node]
        closed_set = set()

        while open_set:
            current_node = heapq.heappop(open_set)
            closed_set.add(current_node.position)

            if current_node.position == self.goal:
                path = []
                while current_node.parent:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]

            for neighbor in self.get_neighbors(current_node):
                if neighbor.position in closed_set:
                    continue

                tentative_cost = current_node.cost + 1
                neighbor.cost = tentative_cost
                neighbor.heuristic = self.heuristic(neighbor.position, self.goal)

                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)

        return None
   
    def draw_maze(self, path=None):
        # Create the Tkinter window
        root = tk.Tk()
        root.title("Maze Solver")

        # Initialize MazeCanvas
        maze_canvas = MazeCanvas(root, self.maze, self.start, self.goal)       

        # Draw the maze on the canvas
        maze_canvas.canvas.delete("all")
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                x0, y0 = j * 30, i * 30
                x1, y1 = (j + 1) * 30, (i + 1) * 30

                if (i, j) == self.start:
                    maze_canvas.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                elif (i, j) == self.goal:
                    maze_canvas.canvas.create_rectangle(x0, y0, x1, y1, fill="red")
                elif path and (i, j) in path:
                    maze_canvas.canvas.create_rectangle(x0, y0, x1, y1, fill="yellow")
                elif cell == 0:
                    maze_canvas.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                else:
                    maze_canvas.canvas.create_rectangle(x0, y0, x1, y1, fill="black")

        # Run the Tkinter main loop
        root.mainloop()

    def update_maze(self):
        solution_path = self.a_star()
        self.draw_maze(solution_path)