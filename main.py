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

    cd = ConstellationBuilder()
    #Constallation Object
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

    #Crop
    # img = crop_image(gray, img, 40)

    # cv2.imshow('Finished Product', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    