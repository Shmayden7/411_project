import random
import copy
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def heuristic(state, target_state):
    total_distance = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            value = state[i][j]
            if value != 0:
                target_row, target_col = divmod(value - 1, size)
                total_distance += abs(i - target_row) + abs(j - target_col)
    return total_distance

def get_neighbors(node):
    neighbors = []
    size = len(node.state)
    for i in range(size):
        for j in range(size):
            if node.state[i][j] == 0:
                moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for di, dj in moves:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < size and 0 <= nj < size:
                        new_state = [list(row) for row in node.state]
                        new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                        neighbors.append(PuzzleNode(new_state, parent=node, move=(i, j)))
    return neighbors

def a_star(initial_state, target_state, stop_state=None):
    start_node = PuzzleNode(initial_state)
    start_node.heuristic = heuristic(start_node.state, target_state)

    open_set = [start_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)
        closed_set.add(tuple(map(tuple, current_node.state)))

        if current_node.state == target_state:
            path = []
            while current_node.parent:
                path.append(current_node.move)
                current_node = current_node.parent
            return path[::-1]

        if stop_state is not None and current_node.state == stop_state:
            # Return the current path when the stop state is reached
            path = []
            while current_node.parent:
                path.append(current_node.move)
                current_node = current_node.parent
            return path[::-1]

        for neighbor in get_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) in closed_set:
                continue

            tentative_cost = current_node.cost + 1
            neighbor.cost = tentative_cost
            neighbor.heuristic = heuristic(neighbor.state, target_state)

            if neighbor not in open_set:
                heapq.heappush(open_set, neighbor)

    return None

def print_puzzle(state):
    for row in state:
        print(" ".join(map(str, row)))

def generate_random_puzzle(size):
    flat_puzzle = list(range(size * size))
    random.shuffle(flat_puzzle)
    return [flat_puzzle[i:i+size] for i in range(0, size*size, size)]

def visualize_moves(initial_state, moves):
    """
    Visualize the moves using NetworkX and Matplotlib.

    Parameters:
    - initial_state: The initial state of the puzzle.
    - moves: The list of moves in the solution path.
    """
    G = nx.DiGraph()
    pos = {}

    current_state = initial_state
    for i, move in enumerate(moves):
        G.add_node(i, label=f"Move {i + 1}\n{move}")

        new_state = copy.deepcopy(current_state)
        empty_i, empty_j = move
        current_i, current_j = [index for index, row in enumerate(new_state) if 0 in row][0], new_state[empty_i][empty_j]
        new_state[empty_i][empty_j], new_state[current_i][current_j] = new_state[current_i][current_j], 0

        pos[i] = {tuple(map(tuple, [(j, -i) for j, state in enumerate(row)])): (j, -i) for i, row in enumerate(new_state) for j, state in enumerate(row)}

        if i > 0:
            G.add_edge(i - 1, i)

        current_state = new_state
        i=i-1

    labels = nx.get_edge_attributes(G, "label")
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, "label"), node_size=7000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="red")
    plt.show()

# Example usage for a 3x3 slider puzzle
if __name__ == "__main__":
    # Example target state
    target_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # Generate a random initial state
    initial_state = generate_random_puzzle(len(target_state))

    print("Initial state:")
    print_puzzle(initial_state)

    print("\nTarget state:")
    print_puzzle(target_state)

    # Solve the puzzle
    solution_path = a_star(initial_state, target_state)

    if solution_path:
        print("\nOptimized Solution Path:")
        for move in solution_path:
            print(f"Move empty tile to position: {move}")
        visualize_moves(initial_state, solution_path)
    else:
        print("\nNo solution found.")