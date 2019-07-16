import cv2
import numpy as np
from shapedetector import ShapeDetector
import matplotlib.pyplot as plt

def crop_image(gray, img,tol=0):
    # img is image data
    # tol  is tolerance
    mask = gray>tol
    return img[np.ix_(mask.any(1),mask.any(0))]

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

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
    lines = shapedetector.detect_lines(img)

    fig, ax = plt.subplots() 
    plt.scatter(x, y)
    # plt.axis([-2, 2, -2, 2]) # TODO have this as scale returned from detect_stars and detect_lines
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]))
    # for line in lines:
    #     x1 = find_nearest(x, line.item(0))
    #     x2 = find_nearest(x, line.item(2))
    #     y1 = find_nearest(y, -line.item(1))
    #     y2 = find_nearest(y, -line.item(3))
    #     plt.plot((x1, x2), (y1, y2), 'ro-', linewidth=2, markersize=0)
    for line in lines:
        plt.plot((line.item(0), line.item(2)), (-line.item(1), -line.item(3)), 'ro-', linewidth=2, markersize=0)

    plt.show()

    #Crop
    img = crop_image(gray, img, 40)

    # cv2.imshow('Finished Product', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    