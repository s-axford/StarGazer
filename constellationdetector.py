from helper import straighten
import matplotlib.pyplot as plt
from shapedetector import ShapeDetector
import numpy as np
import math

class ConstellationDetector:
    consellations = []
    def __init__(self, consellations_array):
        consellations = consellations_array

    def search_for_constellation(self, con, x, y, mags):
        sd = ShapeDetector()
        l1, l2 = sd.find_brightest_stars(mags)
        x0, x1 = x[l1], x[l2]
        y0, y1 = y[l1], y[l2]
        dx = x1 - x0
        dy = y1 - y0
        # Shift for angle
        angle = 90*(1-np.sign(dx)) + math.atan(dy/dx)
        rotation_matrix = np.array([[math.cos(angle), math.sin(angle)],[-math.sin(angle), math.cos(angle)]])
        position_matrix = np.array([con.stars_x, con.stars_y])
        brightest = np.array([x0, y0])
        result = np.matmul(rotation_matrix, position_matrix)
        # result = np.add(result, brightest)
        cx = result[0]
        cy = result[1]
        fig, ax = plt.subplots()
        plt.scatter(x, y)
        plt.scatter(cx, cy)
        for i, txt in enumerate(con.stars_mags):
            ax.annotate(2*txt, (x[i], y[i]))
        plt.show()