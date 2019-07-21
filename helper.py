import numpy as np
import math
from scipy.stats import rankdata

def order_mags(mags):
    vals = mags.copy()
    sorted_mags = np.argsort(vals)
    return sorted_mags[::-1]

    
#Take magnitiude array of an image and returns the index of the largest stars
def find_brightest_stars(mags):
    #mag values
    first_largest = 0
    second_largest = 0
    #index of brightest stars
    l1 = -1
    l2 = -1
    for i, mag in enumerate(mags):
        if(mag > first_largest):
            second_largest = first_largest
            l2 = l1
            first_largest = mag
            l1 = i
        elif(mag > second_largest):
            second_largest = mag
            l2 = i
    return l1, l2


# Straightens stars to aling two brightest stars on the x-axis
#returns straighten star locations
def straighten(x, y, mags):
    sorted_mags = order_mags(mags)
    l1, l2 = sorted_mags[0], sorted_mags[1]
    dx = x[l2] - x[l1]
    dy = y[l2] - y[l1]
    angle = 90*(1-np.sign(dx)) + math.atan(dy/dx)
    rotation_matrix = np.array([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])
    position_matrix = np.array([x, y])
    result = np.matmul(rotation_matrix, position_matrix)
    x = result[0]
    y = result[1]
    return x, y, angle

# scales x and y values by dividing by the scale
# scale - scale difference between the test image and template
def scale(x, y, scale):
    for i in range(len(x)):
        x[i] /= scale
        y[i] /= scale
    return x, y


# formats lines to x and y lists
def format_lines_for_manipulation(lines):
    result_x = []
    result_y = []
    for i in lines:
        for x1, y1, x2, y2 in i:
            result_x.append(x1)
            result_x.append(x2)
            result_y.append(y1)
            result_y.append(y2)
    return np.array([result_x, result_y])


# reverts format_lines_for_manipulation
def revert_line_formatting(x, y):
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


# shifts x and y by provided amount
# x and y must have same length
def shift_to_coordinates(x, y, x_coordinate, y_coordinate):
    for i in range(len(x)):
        x[i] -= x_coordinate
        y[i] -= y_coordinate
    return x, y


# straightens lines to match stars
def format_lines_for_presentation(lines, angle, shift, scale_factor=None):
    formatted_lines = format_lines_for_manipulation(lines)
    result = np.matmul(np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]),
                       formatted_lines)
    # Scale if a factor is provided
    if scale_factor is not None:
        result[0], result[1] = scale(result[0], result[1], scale_factor)

    result[0], result[1] = shift_to_coordinates(result[0], result[1], shift[0], -shift[1])
    x = revert_line_formatting(result[0], result[1])
    return x
