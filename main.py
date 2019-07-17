import cv2
import numpy as np
from shapedetector import ShapeDetector
from constellation import Constellation
from constellationbuilder import ConstellationBuilder
import matplotlib.pyplot as plt

def crop_image(gray, img,tol=0):
    # img is image data
    # tol  is tolerance
    mask = gray>tol
    return img[np.ix_(mask.any(1),mask.any(0))]

def main():
    sd = ShapeDetector()
    cd = ConstellationBuilder()
    # Constallation Object
    ursa_major = cd.build_ursa_major()
    constellations = cd.build_all()
    for constellation in constellations:
        constellation.dump_info()
        fig, ax = plt.subplots() 
        plt.scatter(constellation.stars_x, constellation.stars_y)
        # plt.axis([-2, 2, -2, 2]) # TODO have this as scale returned from detect_stars and detect_lines
        for i, txt in enumerate(constellation.stars_mags):
            ax.annotate(txt, (constellation.stars_x[i], constellation.stars_y[i]))
    
        for line in constellation.lines:
            plt.plot((line.item(0), line.item(2)), (-line.item(1), -line.item(3)), 'ro-', linewidth=2, markersize=0)

        plt.show()

    # Read in Image
    img = cv2.imread('DemoImages/ursa_major.png', cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Threshold to binary
    thresh = 100
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]  
    stars = sd.get_all(img)
    x,y,mags = sd.detect_stars(stars)
    fig, ax = plt.subplots() 
    plt.scatter(x, y)
    # plt.axis([-2, 2, -2, 2]) # TODO have this as scale returned from detect_stars and detect_lines
    for i, txt in enumerate(mags):
        ax.annotate(2*txt, (x[i], y[i]))
    plt.show()
    
    #Crop
    # img = crop_image(gray, img, 40)

    cv2.imshow('Finished Product', stars)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    