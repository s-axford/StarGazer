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
