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
    rotation_matrix = np.array([[math.cos(angle), math.sin(angle)],[-math.sin(angle), math.cos(angle)]])
    position_matrix = np.array([x, y])
    result = np.matmul(rotation_matrix, position_matrix)
    x = result[0]
    y = result[1]
    return x,y
