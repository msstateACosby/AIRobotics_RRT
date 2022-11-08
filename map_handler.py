import numpy as np
import cv2 as cv


def discretize_image(file_name, discrete_res):
    img = cv.cvtColor(cv.imread(file_name), cv.COLOR_BGR2GRAY)
    discrete_map = np.zeros(discrete_res)
    for x in range((discrete_map.shape[0])):
        for y in range((discrete_map.shape[1])):
            i = int(x/discrete_map.shape[0] * img.shape[0])
            j = int(y/discrete_map.shape[1] * img.shape[1])
            discrete_map[x,y] = (img[i,j] > 100) * 100
           
    return discrete_map


def main():
    file_name = input("Input file name: ")
    map_x = int(input('Input Discrete X Size: '))
    map_y = int(input('Input Discrete Y Size: '))
    discrete_map = discretize_image(file_name, (map_x, map_y))
    cv.imshow("Map", discrete_map)
    cv.waitKey()


if __name__ == "__main__":
    main()
