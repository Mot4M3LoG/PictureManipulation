from PIL import Image
import numpy as np
import math
import time


def to_gray(image):
    yoda = Image.open(image)
    yoda_array = np.asarray(yoda)

    height, width = yoda.size

    yoda_gray_array = np.full((width, height, 3), 0)

    for i in range(width):
        for j in range(height):
            value = yoda_array[i][j][0] / 3 + yoda_array[i][j][1] / 3 + \
                    yoda_array[i][j][2] / 3
            for k in range(3):
                yoda_gray_array[i][j][k] = value

    gray_yoda = Image.fromarray(yoda_gray_array.astype(np.uint8))
    return gray_yoda


def gray_to_binary_1thr():
    gray_yoda = Image.open('gray_yoda.png')
    yoda_array = np.asarray(gray_yoda)

    height, width = gray_yoda.size

    yoda_binary = np.full((width, height, 3), 0)
    threshold = 150

    for i in range(width):
        for j in range(height):
            if yoda_array[i][j][0] >= threshold:
                for k in range(3):
                    yoda_binary[i][j][k] = 255
            else:
                for k in range(3):
                    yoda_binary[i][j][k] = 0

    binary_yoda = Image.fromarray(yoda_binary.astype(np.uint8))
    binary_yoda.save("binary_yoda(1thr).png")


def gray_to_binary_2thr():
    gray_yoda = Image.open('gray_yoda.png')
    yoda_array = np.asarray(gray_yoda)

    height, width = gray_yoda.size
    threshold1, threshold2 = 80, 160

    yoda_binary = np.full((width, height, 3), 0)

    for i in range(width):
        for j in range(height):
            if yoda_array[i][j][0] >= threshold2:
                for k in range(3):
                    yoda_binary[i][j][k] = 255
            elif yoda_array[i][j][0] <= threshold1:
                for k in range(3):
                    yoda_binary[i][j][k] = 255
            else:
                for k in range(3):
                    yoda_binary[i][j][k] = 0

    binary_yoda = Image.fromarray(yoda_binary.astype(np.uint8))
    binary_yoda.save("binary_yoda(2thr).png")


def histogram_equalization():
    gray_yoda = Image.open('gray_yoda.png')
    yoda_array = np.asarray(gray_yoda)

    height, width = gray_yoda.size
    sum_pixels = height * width

    yoda_1dim = np.ndarray.flatten(yoda_array)
    temp_array = np.bincount(yoda_1dim) / 3
    min_value = min(temp_array)

    equaliz_arr = np.full((256, 3), 0)
    yoda_histed = np.full((width, height, 3), 0)
    sum_previous = 0

    for x in range(256):
        equaliz_arr[x][0] = x
        equaliz_arr[x][1] = temp_array[x] + sum_previous
        sum_previous += temp_array[x]
        equaliz_arr[x][2] = math.ceil((equaliz_arr[x][1] - min_value) / (
                sum_pixels - min_value) * 255)

    for i in range(width):
        for j in range(height):
            pixel_change = yoda_array[i][j][0]
            for k in range(3):
                yoda_histed[i][j][k] = equaliz_arr[pixel_change][2]

    hist_yoda = Image.fromarray(yoda_histed.astype(np.uint8))
    hist_yoda.save("histogram_yoda.png")


def preprocess():
    road = Image.open('gray_road.png')
    road_array = np.asarray(road)
    height, width = road.size

    road_empty = np.full((width, height), 0)

    for i in range(width):
        for j in range(height):
            road_empty[i][j] = road_array[i][j][0]

    road_ready = road_empty.cumsum(axis=0).cumsum(axis=1)
    return road_empty, road_ready, height, width


def blurring():
    road_empty, summed_table, height, width = preprocess()

    road_blurred = np.copy(road_empty)

    for i in range(35, width - 35):
        for j in range(35, height - 35):
            road_blurred[i][j] = (summed_table[i + 35][j + 35] -
                                  summed_table[i - 35][
                                      j + 35] - summed_table[i + 35][j - 35] +
                                  summed_table[i - 35][j - 35]) \
                                 / 5041

    road_filtered = Image.fromarray(road_blurred.astype(np.uint8))
    road_filtered.save("road_filtered.png")


def blurring_naive():
    road = Image.open('gray_road.png')
    road_array = np.asarray(road)
    height, width = road.size

    road_empty = np.full((width, height), 0)

    for i in range(width):
        for j in range(height):
            road_empty[i][j] = road_array[i][j][0]

    road_blurred = np.copy(road_empty)

    for i in range(35, width - 35):
        print(i)
        for j in range(35, height - 35):
            x = np.nanmean(road_empty[i-35:i+35, j-35:j+35])
            road_blurred[i][j] = int(x)

    road_filtered = Image.fromarray(road_blurred.astype(np.uint8))
    road_filtered.save("road_filtered(naive).png")


#  yoda_in_gray = to_gray("yoda.jpeg")
#  yoda_in_gray.save("gray_yoda.png")

#  gray_to_binary_1thr()

#  gray_to_binary_2thr()

#  histogram_equalization()
# --------------------
#  road_in_gray = to_gray("road.jpg")
#  road_in_gray.save("gray_road.png")

#  start_time = time.time()
#  blurring()
#  end_time = time.time()
#  print("time with summed table: " + str(end_time - start_time) + " seconds\n")

#  start_time2 = time.time()
#  blurring_naive()
#  end_time2 = time.time()
#  print("time with no table: " + str(end_time2 - start_time2) + " seconds")
