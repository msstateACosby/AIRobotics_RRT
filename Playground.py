import numpy as np

class Node:
    # position should be a numpy array
    # cost is the distance between this node and its parent only
    def __init__(self, parent, children, cost, position):
        self.parent = parent
        self.children = children
        self.cost = cost
        self.position = position

def tree_traversal(root, points, depth=0):
    if depth == 0:
        points.append(root)
    if root.children:
        for i in range(len(root.children)):
            points.append(root.children[i])
            tree_traversal(root.children[i], points, depth+1)
   

root = Node(None, [], 0, (0,0))

root.children.append(Node(root, [], 0, (1,1)))

root.children.append(Node(root, [], 0, (2,2)))

points = []

tree_traversal(root, points)

print(points)