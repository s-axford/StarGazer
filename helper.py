import numpy as np
import math
from shapedetector import ShapeDetector

# Straightens stars to aling two brightest stars on the x-axis
#returns straighten star locations
def straighten(x, y, mags):
    sd = ShapeDetector()
    l1, l2 = sd.find_brightest_stars(mags)
    dx = x[l2] - x[l1]
    dy = y[l2] - y[l1]
    angle = 90*(1-np.sign(dx)) + math.atan(dy/dx)
    rotation_matrix = np.array([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])
    position_matrix = np.array([x, y])
    result = np.matmul(rotation_matrix, position_matrix)
    x = result[0]
    y = result[1]
    return x, y, angle


# formats lines to x and y lists
def format_lines(lines):
    result_x = []
    result_y = []
    for i in lines:
        for x1, y1, x2, y2 in i:
            result_x.append(x1)
            result_x.append(x2)
            result_y.append(y1)
            result_y.append(y2)
    return np.array([result_x, result_y])


# reverts format_lines
def reformat_lines(x, y):
    lines = []
    i = 0
    row = []
    for item in range(len(x)):
        row.append(x[item])
        row.append(y[item])
        i += 1
        if i == 2:
            i = 0
            lines.append([row])
            row = []
    return np.array(lines)


# straightens lines to match stars
def straighten_lines(lines, angle):
    formatted_lines = format_lines(lines)
    result = np.matmul(np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]),
                       formatted_lines)
    x = reformat_lines(result[0], result[1])
    return x
