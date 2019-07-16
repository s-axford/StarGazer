import cv2
import numpy as np
from shapedetector import ShapeDetector
import matplotlib.pyplot as plt

def crop_image(gray, img,tol=0):
    # img is image data
    # tol  is tolerance
    mask = gray>tol
    return img[np.ix_(mask.any(1),mask.any(0))]

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

    #Find stars
    shapedetector = ShapeDetector()
    x, y, labels = shapedetector.detect_stars(img)
    cv2.imshow('Finished Product', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    shapedetector.detect_lines(img)

    print(labels)
    fig, ax = plt.subplots() 
    plt.scatter(x, y)
    # plt.axis([-2, 2, -2, 2]) // TODO have this as scale returned from detect_stars and detect_lines
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]))
    plt.show()

    #Crop
    img = crop_image(gray, img, 40)

    cv2.imshow('Finished Product', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    