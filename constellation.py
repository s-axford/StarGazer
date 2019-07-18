import numpy as np
import math
from shapedetector import ShapeDetector

class Constellation:
    stars_x = []
    stars_y = []
    stars_mags = []
    lines = []
    number_of_stars = 0

    def __init__(self, x, y, mag, cons_lines):
        self.stars_x = x
        self.stars_y = y
        self.stars_mags = mag
        self.lines = cons_lines
        self.number_of_stars = len(mag)
    
    def dump_info(self):
        print(self.stars_x)
        print(self.stars_y)
        print(self.stars_mags)
        print(self.lines)

    def straighten(self):
        sd = ShapeDetector()
        l1, l2 = sd.find_brightest_stars(self.stars_mags)
        dx = self.stars_x[l2] - self.stars_x[l1]
        dy = self.stars_y[l2] - self.stars_y[l1]
        angle = 90*(1-np.sign(dx)) + math.atan(dy/dx)
        rotation_matrix = np.array([[math.cos(angle), math.sin(angle)],[-math.sin(angle), math.cos(angle)]])
        position_matrix = np.array([self.stars_x,self.stars_y])
        # brightest_star = np.array([[self.stars_x[l1]],[self.stars_y[l1]]])
        result = np.matmul(rotation_matrix, position_matrix)
        self.stars_x = result[0]
        self.stars_y = result[1]
        print('-------------------------')
        print(angle)
        print(rotation_matrix)
        print(position_matrix)
        print(result)
        print('-------------------------')