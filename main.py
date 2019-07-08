import cv2
import numpy as np
from shapedetector import ShapeDetector

def main():
    # Read in Image
    img = cv2.imread('DemoImages/UrsaMajor.jpg', cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Threshold to binary
    thresh = 100
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]  

    #Isolated unwanted text elements
    text = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]  
    dilated = cv2.dilate(text, np.ones((11, 11)))
    #Remove text elements leaving only stars in red and lines in blue
    img[dilated > 250] = 0
    
    #Show image
    cv2.imshow('Constallation', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #Find stars
    shapedetector = ShapeDetector()
    shapedetector.detect(img)
    
    cv2.imshow('Finished Product', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    