import cv2
import numpy as np
from shapedetector import ShapeDetector
from constellation import Constellation
from operator import itemgetter, attrgetter
import glob

class ConstellationBuilder:
    def build_ursa_major(self):
        # Read in Image
        img = cv2.imread('Constellations/UrsaMajor.jpg', cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Threshold to binary
        thresh = 100
        img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]  

        #Isolated unwanted text elements
        text = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]  
        dilated = cv2.dilate(text, np.ones((11, 11)))
        #Remove text elements leaving only stars in red and lines in blue
        img[dilated > 250] = 0

        #Find stars
        shapedetector = ShapeDetector()
        stars = shapedetector.get_stars(img)
        x, y, mags = shapedetector.detect_stars(stars)
        lines = shapedetector.detect_lines(img)
        con = Constellation(x, y, mags, lines)
        con.align_constellation()
        return Constellation(x,y,mags,lines)

    def build_all(self):
        constellations = []
        for filename in glob.glob('Constellations/*.jpg'):
            # Read in Image
            img = cv2.imread(filename, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Threshold to binary
            thresh = 100
            img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]  
    
            # Isolated unwanted text elements
            text = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]  
            dilated = cv2.dilate(text, np.ones((11, 11)))
            # Remove text elements leaving only stars in red and lines in blue
            img[dilated > 250] = 0
    
            # Find stars
            shapedetector = ShapeDetector()
            stars = shapedetector.get_stars(img)
            x, y, mags = shapedetector.detect_stars(stars)
            lines = shapedetector.detect_lines(img)
            con = Constellation(x, y, mags, lines)
            con.align_constellation()
            constellations.append(con)
        return sorted(constellations, key=attrgetter('number_of_stars'))

