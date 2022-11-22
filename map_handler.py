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


def select_start_and_goal(discrete_map):
    x, y = discrete_map.shape
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
    # Enumeration of maps and their sizes
    maps = [
            ("house.png", (500, 500)),
            ("map_1.png", (1920, 1080)),
            ("map_2.png", (1920, 1080)),
            ("map_3.png", (1920, 1080)),
            ("map_4.png", (1920, 1080)),
            ]
    #
    ####

    selected_map = maps[0]

    image = cv.cvtColor(cv.imread(selected_map[0]), cv.COLOR_BGR2GRAY)

    size = (selected_map[1][1], selected_map[1][0])

    #discrete_map = discretize_image(image, size)
    discrete_map = image

    start, end = select_start_and_goal(discrete_map)
    points = RRT(250, discrete_map, start, end)
    image = discrete_map
    print(image.shape)
    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    line_thickness = 1
    point_thickness = 7
    wait_time = 1000

    # Open in color to display red line
    #image = cv.imread(selected_map[0])

    image = cv.circle(image, start, point_thickness, green, -1)
    image = cv.circle(image, end, point_thickness, green, -1)
    cv.imshow("Map", image)
    cv.waitKey(wait_time)
    for p, _ in enumerate(points):
        if p + 1 >= len(points):
            break
        
        pair = (points[p], points[p+1])

        image = cv.line(image, pair[0], pair[1], red, line_thickness)
        cv.imshow("Map", image)
        cv.waitKey(wait_time)

    cv.imshow("Map", image)
    cv.waitKey()


if __name__ == "__main__":
    main()
