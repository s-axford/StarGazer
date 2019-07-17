import cv2
import numpy as np
from shapedetector import ShapeDetector
from constellation import Constellation
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
        x, y, mags = shapedetector.detect_stars(img)
        lines = shapedetector.detect_lines(img)
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
            x, y, mags = shapedetector.detect_stars(img)
            lines = shapedetector.detect_lines(img)
            constellations.append(Constellation(x, y, mags, lines))
        return constellations