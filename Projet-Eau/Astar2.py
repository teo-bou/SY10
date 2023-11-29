from typing import List, Tuple
from heapq import heappop, heappush
import main
from Objets import *
import warnings

#suppress warnings
warnings.filterwarnings('ignore')
class Node:
    """
    Class to represent a node in the map.

    Attributes:
    - position: Tuple[int, int]
        The (x, y) coordinates of the node in the map.
    - g: float
        The cost from the start node to this node.
    - h: float
        The estimated cost from this node to the goal node.
    - f: float
        The total cost of the node (g + h).
    - parent: Node
        The parent node from which this node is reached.
    """

    def __init__(self, position: Tuple[int, int]):
        """
        Constructor to instantiate the Node class.

        Parameters:
        - position: Tuple[int, int]
            The (x, y) coordinates of the node in the map.
        """

        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        """
        Less than comparison operator for nodes.

        This is used for comparing nodes in the priority queue.

        Parameters:
        - other: Node
            The other node to compare with.

        Returns:
        - bool:
            True if this node has a lower f value than the other node, False otherwise.
        """

        return self.f < other.f


def calculate_heuristic(map, current: Tuple[int, int], goal: Tuple[int, int]) -> float:
    """
    Calculates the heuristic value (estimated cost) between two nodes.

    In this case, we use the Manhattan distance as the heuristic.

    Parameters:
    - current: Tuple[int, int]
        The (x, y) coordinates of the current node.
    - goal: Tuple[int, int]
        The (x, y) coordinates of the goal node.

    Returns:
    - float:
        The estimated cost between the current and goal nodes.
    """

    return abs(current[0] - goal[0]) + abs(current[1] - goal[1]) + 15*map.alt_cum(Point(current), Point(goal))


def get_neighbors(current: Tuple[int, int], map_size: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Returns the valid neighboring nodes of a given node.

    Parameters:
    - current: Tuple[int, int]
        The (x, y) coordinates of the current node.
    - map_size: Tuple[int, int]
        The size of the map (number of rows, number of columns).

    Returns:
    - List[Tuple[int, int]]:
        A list of valid neighboring nodes.
    """

    neighbors = []
    x, y = current

    # Check the four cardinal directions
    if x > 0:
        neighbors.append((x - 1, y))
    if x < map_size[0] - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < map_size[1] - 1:
        neighbors.append((x, y + 1))

    return neighbors


def search_map_with_portals(map: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> List[
    Tuple[int, int]]:
    """
    Searches the map using the A* algorithm with support for portals.

    Parameters:
    - map: List[List[int]]
        The map represented as a 2D grid of integers.
        0 represents an obstacle, and any other positive integer represents a portal.
    - start: Tuple[int, int]
        The (x, y) coordinates of the start node.
    - goal: Tuple[int, int]
        The (x, y) coordinates of the goal node.

    Returns:
    - List[Tuple[int, int]]:
        A list of (x, y) coordinates representing the path from the start to the goal node.
        If no path is found, an empty list is returned.
    """

    # Check if the start or goal nodes are out of bounds
    if start[0] < 0 or start[0] >= map.l or start[1] < 0 or start[1] >= map.L:
        raise ValueError("Start node is out of bounds.")
    if goal[0] < 0 or goal[0] >= map.l or goal[1] < 0 or goal[1] >= map.L:
        raise ValueError("Goal node is out of bounds.")


    # Initialize the open and closed lists
    open_list = []
    closed_list = set()

    # Create the start and goal nodes
    start_node = Node(start)
    goal_node = Node(goal)

    # Calculate the heuristic value for the start node
    start_node.h = calculate_heuristic(map, start, goal)
    start_node.f = start_node.h

    # Add the start node to the open list
    heappush(open_list, start_node)

    # Start the A* algorithm
    while open_list:
        # Get the node with the lowest f value from the open list
        current_node = heappop(open_list)

        # Check if the current node is the goal node
        if current_node.position == goal:
            # Reconstruct the path from the goal node to the start node
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Reverse the path to get it from start to goal

        # Add the current node to the closed list
        closed_list.add(current_node.position)

        # Get the neighboring nodes of the current node
        neighbors = get_neighbors(current_node.position, (map.l, map.L))

        for neighbor in neighbors:
            # Check if the neighbor is an obstacle or already in the closed list
            if neighbor in closed_list:
                continue

            # Create a new node for the neighbor
            neighbor_node = Node(neighbor)

            # Calculate the cost from the start node to the neighbor node
            neighbor_node.g = current_node.g + 1

            # Calculate the heuristic value for the neighbor node
            neighbor_node.h = calculate_heuristic(map, neighbor, goal)

            # Calculate the total cost of the neighbor node
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # Set the parent of the neighbor node
            neighbor_node.parent = current_node

            # Add the neighbor node to the open list
            heappush(open_list, neighbor_node)

    # No path found
    return []


# Example usage:



# Define the start and goal nodes
start = (main.S.x, main.S.y)
goal = (main.ZZ.x, main.ZZ.y)

# Search the map using A* algorithm with portals
path = search_map_with_portals(main.carte, start, goal)
x = [point[0] for point in path]
y = [point[1] for point in path]
plt.plot(x,y)
plt.show()
plt.plot([main.carte.alt(point) for point in path])
plt.show()
# Print the path
print(path)
# if path:
#     print("Path found:")
#     for node in path:
#         print(node)
# else:
#     print("No path found.")