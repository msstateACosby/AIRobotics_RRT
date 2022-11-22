import random
import numpy as np
import cv2 as cv
from RRT_Star import RRT


def discretize_image(img, discrete_res):
    discrete_map = np.zeros(img.shape)
    for x in range(discrete_map.shape[0] - 1):
        for y in range(discrete_map.shape[1] - 1):
            i = int(x/discrete_map.shape[0] * img.shape[0])
            j = int(y/discrete_map.shape[1] * img.shape[1])
            discrete_map[x,y] = (img[i,j] > 100) * 100
            #discrete_map[x,y] = (img[x,y] > 100) * 100
           
    #for row in discrete_map:
        #print(row)
    #exit()
    print(img.shape)
    print(discrete_map.shape)
    return discrete_map

def tree_traversal_drawing(root, image):
    blue = (255, 0, 0)
    if root.children:
        for node in root.children:
            cv.line(image, root.position, node.position, blue, 1)
            tree_traversal_drawing(node, image)


def select_start_and_goal(discrete_map):
    x, y = discrete_map.shape
    print(f"{x=}, {y=}")
    x -= 1
    y -= 1

    # Ensure you're at least 5% from the edge
    x_pct = round(x / 100 * 5)
    y_pct = round(y / 100 * 5)

    x -= x_pct
    y -= y_pct

    start = (random.randint(x_pct, x), random.randint(y_pct, y))
    while discrete_map[start] == 0:
        start = (random.randint(x_pct, x), random.randint(y_pct, y))

    end = (random.randint(x_pct, x), random.randint(y_pct, y))
    while discrete_map[end] == 0:
        end = (random.randint(x_pct, x), random.randint(y_pct, y))

    return start, end


def main():
    ####
    # Enumeration of map files, sizes, distance thresholds, and iteration counts
    iterations = 2000
    maps = [
            ("house.png", (500, 500), 20, iterations),
            ("map_1.png", (1920, 1080), 100, iterations),
            ("map_2.png", (1920, 1080), 100, iterations),
            ("map_3.png", (1920, 1080), 100, iterations),
            ("map_4.png", (1920, 1080), 100, iterations),
            ("map_5.png", (512, 512), 50, iterations),
            ]
    #
    ####

    selected_map = maps[5]

    image = cv.imread(selected_map[0])
    #size = (selected_map[1][1], selected_map[1][0])
    #discrete_map = discretize_image(image, size)
    discrete_map = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


    start, end = select_start_and_goal(discrete_map)
    points, root = RRT(selected_map[2], selected_map[3], discrete_map, start, end)
    start = (start[1], start[0])
    end = (end[1], end[0])
    print(f"{start=}, {end=}")
    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    line_thickness = 2
    point_thickness = 4
    wait_time = 1000

    image = cv.circle(image, start, point_thickness, green, -1)
    image = cv.circle(image, end, point_thickness, blue, -1)
    cv.imshow("Map", image)
    cv.waitKey(wait_time)
    tree_traversal_drawing(root, image)
    for p, _ in enumerate(points):
        if p + 1 >= len(points):
            break
        
        #pair = ((points[p][1], points[p][0]), (points[p+1][1], points[p+1][0]))
        pair = (points[p], points[p + 1])

        image = cv.line(image, pair[0], pair[1], red, line_thickness)
        cv.imshow("Map", image)
        cv.waitKey(wait_time)

    cv.imshow("Map", image)
    cv.waitKey()


if __name__ == "__main__":
    main()
