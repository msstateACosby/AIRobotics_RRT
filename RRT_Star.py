import numpy as np

class Node:
    # position should be a numpy array
    # cost is the distance between this node and its parent only
    def __init__(self, parent, children, cost, position):
        self.parent = parent
        self.children = children
        self.cost = cost
        self.position = position

    def __lt__(self, other):
        return self.cost < other.cost

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

    node_neighbors.sort(key=lambda x : x.cost)
        
    return node_neighbors

def collides(a, b, discretized_map):
    try:
        slope = (b.position[0]-a.position[0])/(b.position[1]-a.position[1])
        if a.position[1] < b.position[1]:
            x_values = np.array(list(range(a.position[1],b.position[1]+1)))
            y_values = slope * (x_values - a.position[1]) + a.position[0]
        else:
            x_values = np.array(list(range(b.position[1],a.position[1]+1)))
            y_values = slope * (x_values - b.position[1]) + b.position[0]
        floor_values = np.floor(y_values)
        ceiling_values = np.ceil(y_values)
        for i in range(len(x_values)):
            
            y_start = y_values[i]
            y_end = y_start + slope
            for j in range(int(min(y_start,y_end)), int(max(y_start,y_end))+ 1):
                if discretized_map[int(x_values[i]), int(np.floor(j))] == 0:
                    return True
                if discretized_map[int(x_values[i]), int(np.ceil(j))] == 0:
                    return True
        return False
    except ZeroDivisionError:
        y_values = range(min(a.position[0], b.position[0]), max(a.position[0], b.position[0]))
        x_values = [a.position[1] for _ in range(len(y_values))]
        for i in range(len(x_values)):
            if discretized_map[int(x_values[i]), int(y_values[i])] == 0:
                return True
        return False


def euc_dist(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)

def RRT(threshold, iterations, discretized_map, start, goal):
    start = (start[1], start[0])
    goal = (goal[1], goal[0])
    root = Node(None, [], 0, start)
    goal_node = Node(None, [], 0, goal)

    map_size = discretized_map.shape
    stored_node = None
    # See how the other sub-team handles this to make this generalizable
    old_dist_to_goal = np.inf
    iterations_ran = 0
    while iterations > 0 or stored_node == None:
        iterations_ran += 1
        iterations -= 1
        points = []
        tree_traversal(root, points)
        randomPosition = (np.random.randint(map_size[0]), np.random.randint(map_size[1]))
        new_node = Node(None, [], np.inf, randomPosition)
        if discretized_map[randomPosition] == 0:
            continue
        #nearest_node = nearest(new_node, points)
        #new_node.cost = euc_dist(new_node.position, nearest_node.position)
        # Get a good value for radius, maybe dynamically calculated? Right now it's 16 arbitrarily.
        node_neighbors = find_neighbors(points, new_node, threshold)
        node_best = None
        for node in node_neighbors:
            if not collides(node, new_node, discretized_map):
                node_best = node
                break
        if node_best == None:
            continue
        new_node.parent = node_best
        node_best.children.append(new_node)
        new_node.cost = euc_dist(new_node.position, node_best.position) + node_best.cost
        #print(node_best, new_node, node_best.cost, new_node.cost, node_best.position, new_node.position)
        # Rewire the graph as appropriate for the neighbors of this new node
        for neighbor in node_neighbors:
            if collides(neighbor, new_node, discretized_map):
                continue
            if new_node.cost + euc_dist(new_node.position, neighbor.position) < neighbor.cost:
                neighbor.cost = new_node.cost + euc_dist(new_node.position, neighbor.position)
                neighbor.parent.children.remove(neighbor)
                neighbor.parent = new_node
                new_node.children.append(neighbor)
                #Pseudocode says G += {new_node, neighbor}. What does this mean in our context? Is it necessary?
        # Similarly it says G += Link here. It's assuming the graph is defined in terms of edges and vertices
        dist_to_goal =euc_dist(new_node.position, goal_node.position)
        
        if  dist_to_goal <= threshold and dist_to_goal < old_dist_to_goal and not collides(new_node, goal_node, discretized_map):
            stored_node = new_node
            #print(new_node.position, goal_node.position, collides(new_node, goal_node, discretized_map))
            old_dist_to_goal = dist_to_goal
    
    points = []
    tree_traversal(root, points)


    goal_node = Node(None, [], 0, goal)

    best_node = nearest(goal_node, points)

    path = [best_node.position, stored_node.position, goal]

    current_node = best_node

    while(current_node.parent is not None):
        path.insert(0,current_node.position)
        current_node = current_node.parent

    path.insert(0, start)

    print(f"{iterations_ran} Iterations")
    return path, root, stored_node.cost + old_dist_to_goal
                
