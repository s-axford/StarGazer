from helper import straighten, straighten_lines


class Constellation:
    stars_x = []
    stars_y = []
    stars_mags = []
    lines = []
    rotation_angle = None
    number_of_stars = 0
    brightest_star = ()  # I need this in (x, y) format of the position of the brightest star for moving the lines

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
        self.stars_x, self.stars_y, self.rotation_angle = straighten(self.stars_x, self.stars_y, self.stars_mags)
        self.lines = straighten_lines(self.lines, self.rotation_angle)
