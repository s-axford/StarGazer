from helper import straighten
import matplotlib.pyplot as plt
from helper import find_brightest_stars, shift_to_coordinates, scale
import numpy as np
import math

class ConstellationDetector:
    consellations = []
    def __init__(self, consellations_array):
        consellations = consellations_array

    def search_for_constellation(self, con, x, y, mags):
        # Find brightest star
        l1, l2 = find_brightest_stars(mags)
        x0, x1 = x[l1], x[l2]
        y0, y1 = y[l1], y[l2]
        dx = x1 - x0
        dy = y1 - y0
        
        # Shift for angle
        angle = 90*(1-np.sign(dx)) + math.atan(dy/dx)
        rotation_matrix = np.array([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])
        position_matrix = np.array([con.stars_x, con.stars_y])
        result = np.matmul(rotation_matrix, position_matrix)
        cx, cy = result[0], result[1]

        # Scale template to match test image
        cdx = cx[con.brightest_stars_index[1]] - cx[con.brightest_stars_index[0]]
        test_scale = cdx/dx
        cx, cy = scale(cx, cy, test_scale)

        # Shift template to contellation
        cx, cy = shift_to_coordinates(result[0], result[1], -x0, -y0)

        # Check for match
        matches = self.check_for_matches(cx, cy, x, y, test_scale)
        # If atleast half the stars match, draw the star
        if(matches >= 0.5*len(con.stars_x)):
            return cx, cy, angle, test_scale

        # Plot
        fig, ax = plt.subplots()
        plt.scatter(x, y)
        plt.scatter(cx, cy)
        for i, txt in enumerate(con.stars_mags):
            ax.annotate(2*txt, (x[i], y[i]))
        plt.show()

    # Check for matches returns the amount of stars similar between a template and a image according to a scale
    def check_for_matches(self, temp_x, temp_y, x, y, scale):
        matches = 0
        threshold = 0.15 / scale # 0.15 because science
        for temp_star in range(len(temp_x)):
            for test_star in range(len(x)):
                x_diff = abs(temp_x[temp_star] - x[test_star])
                y_diff = abs(temp_y[temp_star] - y[test_star])
                if(x_diff < threshold and y_diff < threshold):
                    matches += 1
        return matches
