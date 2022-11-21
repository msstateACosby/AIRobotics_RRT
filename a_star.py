import numpy as np
from RRT_Star import Node, euc_dist
import queue
#get the neighbors of a (x,y) position
def get_neighbors(g, grid):
    
    neighbors = [] # The list of successors/neighbors

    possible_neighbors =[
        (g[0] + 1, g[1] - 1),
        (g[0] + 1, g[1]    ),
        (g[0] + 1, g[1] + 1),
        (g[0]    , g[1] + 1),
        (g[0] - 1, g[1] - 1),
        (g[0] - 1, g[1]    ),
        (g[0] - 1, g[1] + 1),
        (g[0]    , g[1] - 1),
    ]
    for neighbor in possible_neighbors:
        if (grid[neighbor[0], neighbor[1]] != 0 and 
            neighbor[0] >= 0 and neighbor[0] < grid.shape[0] and
            neighbor[1] >= 0 and neighbor[1] < grid.shape[1]):
            neighbors.append(neighbor)
    return neighbors  

#actually runs the a_star
def a_star(grid, start, end):
    fringe = queue.PriorityQueue()
    closed = []
    start_node = Node(None, None, 0, start)
    fringe.put((0, start))
    while not fringe.empty():
        current = fringe.get()[1]
        if current.position not in closed:
            if current.position == end:
                return current
            closed.append(current.position)
            neighbors = get_neighbors(current.position, grid)
            for neighbor in neighbors:
                cost_to = euc_dist(neighbor, current.position)
                cum_cost = cost_to + current.cost
                heuristic = euc_dist(neighbor, end)
                priority = cum_cost + heuristic
                new_node = Node(current, None, priority, neighbor)
                fringe.put((priority, new_node))

# adds in the traceback
#calling this returns a list of points describing the path
def run_a_star(grid, start, end):
    path = []
    trace = a_star(grid, start, end)
    while trace.position != start:
        path.append(trace.position)
        trace = trace.parent
    return path[::-1]
