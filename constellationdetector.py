from helper import format_lines_for_presentation
import matplotlib.pyplot as plt
from helper import find_brightest_stars, shift_to_coordinates, scale
import numpy as np
import math

class ConstellationDetector:
    consellations = []
    def __init__(self, consellations_array):
        consellations = consellations_array

    def search_for_constellation(self, con, x, y, mags, l1, l2):
        print("largest stars:")
        print(mags[l1])
        print(mags[l2])
        print(con.brightest_stars_index)
        print(con.stars_mags)
        # Find brightest star
        x0, x1 = x[l1], x[l2]
        y0, y1 = y[l1], y[l2]
        dx = x1 - x0
        dy = y1 - y0

        if dx == 0:
            diff = 0
        else:
            diff = dy/dx
        # Shift for angle
        angle = 90*(1-np.sign(dx)) + math.atan(diff)
        rotation_matrix = np.array([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])
        position_matrix = np.array([con.stars_x, con.stars_y])
        result = np.matmul(rotation_matrix, position_matrix)
        cx, cy = result[0], result[1]

        # Scale template to match test image
        cdx = cx[con.brightest_stars_index[1]] - cx[con.brightest_stars_index[0]]
        test_scale = cdx/dx
        cx, cy = scale(cx, cy, test_scale)

        # Shift template to constellation
        cx, cy = shift_to_coordinates(cx, cy, -x0, -y0)
        print(test_scale)
        # Check for match
        matches = self.check_for_matches(cx, cy, x, y, test_scale)
        print("matches:")
        print(matches)
        print("out of:")
        print(len(con.stars_x))
        plt.scatter(x, y)
        plt.plot(cx, cy, 'y*')
        plt.show()
        # If atleast half the stars match, draw the star
        lines = []
        if matches >= 0.5*len(con.stars_x):
            print("FOUND MATCH")
            lines = format_lines_for_presentation(con.lines, -angle, (-x0, -y0), test_scale)
            return cx, cy, lines, test_scale, True
        return cx, cy, lines, test_scale, False

    # Check for matches returns the amount of stars similar between a template and a image according to a scale
    def check_for_matches(self, temp_x, temp_y, x, y, scale):
        matches = 0
        threshold = 0.10 / scale  # 0.15 because science
        for temp_star in range(len(temp_x)):
            for test_star in range(len(x)):
                x_diff = abs(temp_x[temp_star] - x[test_star])
                y_diff = abs(temp_y[temp_star] - y[test_star])
                if x_diff < threshold and y_diff < threshold:
                    matches += 1
        return matches
