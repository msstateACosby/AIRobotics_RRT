import numpy as np

class Node:
    # position should be a numpy array
    # cost is the distance between this node and its parent only
    def __init__(self, parent, children, cost, position):
        self.parent = parent
        self.children = children
        self.cost = cost
        self.position = position

def nearest_node(this, root):
    # Find the nearest node in the graph (referenced from its root node)
    # Feel free to change this one

def euc_dist(a, b):
    return np.linalg.norm(a - b)

def RRT(iterations, map, start, goal):
    root = Node(None, [], 0, start) 

    map_size = (1000, 1000)
    # See how the other sub-team handles this to make this generalizable

    for i in range(iterations):
        avoids_obst = False
        while(not avoids_obst):
            randomPosition = np.array([np.random.randint(map_size[0]), np.random.randint(map_size[1])])
            new_node = Node(None, [], np.inf, randomPosition)
            if new_node not in map.obstacles:
                avoids_obst = True
        nearest_node = nearest(new_node, root)
        new_node.cost = euc_dist(new_node.position, nearest_node.position)
        # Get a good value for radius, maybe dynamically calculated? Right now it's 16 arbitrarily.
        node_best, node_neighbors = find_neighbors(root, new_node, 16)
        link = chain(new_node, node_best)
        # Rewire the graph as appropriate for the neighbors of this new node
        for neighbor in node_neighbors:
            if new_node.cost + euc_dist(new_node.position, neighbor.position) < neighbor.cost:
                neighbor.cost = new_node.cost + euc_dist(new_node.position, neighbor.position)
                neighbor.parent = new_node
                # Pseudocode says G += {new_node, neighbor}. What does this mean in our context? Is it necessary?
        # Similarly it says G += Link here. It's assuming the graph is defined in terms of edges and vertices
    return root
                
