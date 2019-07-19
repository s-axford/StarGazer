from helper import straighten, format_lines_for_presentation, find_brightest_stars, shift_to_coordinates


class Constellation:
    stars_x = []
    stars_y = []
    stars_mags = []
    lines = []
    number_of_stars = 0
    brightest_stars_index = []

    def __init__(self, x, y, mag, cons_lines):
        self.stars_x = x
        self.stars_y = y
        self.stars_mags = mag
        self.lines = cons_lines
        self.number_of_stars = len(mag)
        l1, l2 = find_brightest_stars(mag)
        self.brightest_stars_index = [l1, l2]
    
    def dump_info(self):
        print(self.stars_x)
        print(self.stars_y)
        print(self.stars_mags)
        print(self.lines)

    def align_constellation(self):
        self.stars_x, self.stars_y, rotation_angle = straighten(self.stars_x, self.stars_y, self.stars_mags)
        brightest_x = self.stars_x[self.brightest_stars_index[0]]
        brightest_y = self.stars_y[self.brightest_stars_index[0]]
        self.stars_x, self.stars_y = shift_to_coordinates(self.stars_x, self.stars_y, brightest_x, brightest_y)
        self.lines = format_lines_for_presentation(self.lines, rotation_angle, (brightest_x, brightest_y))
