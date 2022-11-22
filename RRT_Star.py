import numpy as np

class Node:
    # position should be a numpy array
    # cost is the distance between this node and its parent only
    def __init__(self, parent, children, cost, position):
        self.parent = parent
        self.children = children
        self.cost = cost
        self.position = position

def nearest(this, points):
    # Find the nearest node in the graph
    nearest_node = (None, np.inf)
    for node in points:
        distance = euc_dist(this.position, node.position)
        if distance < nearest_node[1]:
            nearest_node = (node, distance)
    return nearest_node[0]

def tree_traversal(root, points, depth=0):
    if depth == 0:
        points.append(root)
    if root.children:
        for i in range(len(root.children)):
            points.append(root.children[i])
            tree_traversal(root.children[i], points, depth+1)

def find_neighbors(points, new_node, radius):
    node_neighbors = []
    for node in points:
        distance = euc_dist(new_node.position, node.position)
        if distance <= radius:
            node_neighbors.append(node)

    node_neighbors.sort(reverse=True,key=lambda x : x.cost)
        
    return node_neighbors

def collides(a, b, map):
    slope = (b[1]-a[1])/(b[0]-a[0])
    x_values = np.array(list(range(a[0],b[0]+1)))
    y_values = slope * (x_values - a[0]) + a[1]
    floor_values = np.floor(y_values)
    ceiling_values = np.ceiling(y_values)
    for x in x_values:
        for i in range(len(y_values)):
            if map[x, floor_values[i]] != 0:
                return True
            elif map[x, ceiling_values[i]] != 0:
                return True
    return False
                


def euc_dist(a, b):
    return np.linalg.norm(a - b)

def RRT(iterations, map, start, goal):
    root = Node(None, [], 0, start) 

    map_size = map.shape()
    # See how the other sub-team handles this to make this generalizable

    for i in range(iterations):
        points = []
        tree_traversal(root, points)
        randomPosition = np.array([np.random.randint(map_size[0]), np.random.randint(map_size[1])])
        new_node = Node(None, [], np.inf, randomPosition)
        if map[randomPosition] != 0:
            continue
        nearest_node = nearest(new_node, points)
        new_node.cost = euc_dist(new_node.position, nearest_node.position)
        # Get a good value for radius, maybe dynamically calculated? Right now it's 16 arbitrarily.
        node_neighbors = find_neighbors(root, new_node, 16)
        node_best = None
        for node in node_neighbors:
            if not collides(node, new_node, map):
                node_best = node
                break
        if node_best == None: continue
        new_node.parent = node_best
        node_best.children.append(new_node)
        new_node.cost = euc_dist(new_node.position, node_best.position) + node_best.cost
        # Rewire the graph as appropriate for the neighbors of this new node
        for neighbor in node_neighbors:
            if not collides(neighbor, new_node, map): continue
            if new_node.cost + euc_dist(new_node.position, neighbor.position) < neighbor.cost:
                neighbor.cost = new_node.cost + euc_dist(new_node.position, neighbor.position)
                neighbor.parent.children.remove(neighbor)
                neighbor.parent = new_node
                new_node.children.append(neighbor)
                # Pseudocode says G += {new_node, neighbor}. What does this mean in our context? Is it necessary?
        # Similarly it says G += Link here. It's assuming the graph is defined in terms of edges and vertices
    
    points = []
    tree_traversal(root, points)


    goal_node = Node(None, [], 0, goal)

    best_node = nearest(goal_node, points)

    path = [best_node.position,goal]

    current_node = best_node

    while(current_node.parent is not None):
        path.insert(0,current_node.position)
        current_node = current_node.parent

    return path
                
