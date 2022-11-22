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
    #print(possible_neighbors)
    for neighbor in possible_neighbors:
        if (grid[neighbor[1], neighbor[0]] != 0 ):
            neighbors.append(neighbor)
    return neighbors  

#actually runs the a_star
def a_star(grid, start, end):
    fringe = queue.PriorityQueue()
    closed = set()
    start_node = Node(None, None, 0, start)
    fringe.put((0, start_node))
    while not fringe.empty():
        
        current = fringe.get()[1]
        #print(current.position)
        if current.position not in closed:
            if current.position == end:
                return current
            closed.add(current.position)
            neighbors = get_neighbors(current.position, grid)
            for neighbor in neighbors:
                cost_to = euc_dist(neighbor, current.position)
                #print(cost_to)
                cum_cost = cost_to + current.cost
                
                heuristic = euc_dist(neighbor, end)
                priority = cum_cost + heuristic
                #print(cum_cost, heuristic)
                new_node = Node(current, None, cum_cost, neighbor)
                #print(priority)
                fringe.put((priority, new_node))
        #else:
            #print('encounterd before')

# adds in the traceback
#calling this returns a list of points describing the path
def run_a_star(grid, start, end):
    path = []
    
    trace = a_star(grid, start, end)
    cost = trace.cost
    while trace.position != start:
        path.append(trace.position)
        trace = trace.parent
    return path[::-1], cost
