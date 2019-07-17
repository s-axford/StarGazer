class Constellation:
    stars_x = []
    stars_y = []
    stars_mags = []
    lines = []

    def __init__(self, x, y, mag, cons_lines):
        self.stars_x = x
        self.stars_y = y
        self.stars_mags = mag
        self.lines = cons_lines
    
    def dump_info(self):
        print(self.stars_x)
        print(self.stars_y)
        print(self.stars_mags)
        print(self.lines)
