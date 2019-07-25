import cv2
import sys
import numpy as np
from shapedetector import ShapeDetector
from constellationbuilder import ConstellationBuilder
from constellationdetector import ConstellationDetector
import matplotlib.pyplot as plt
from helper import find_brightest_stars, order_mags
from drawing import draw_stars, draw_lines

def crop_image(gray, img,tol=0):
    # img is image data
    # tol  is tolerance
    mask = gray>tol
    return img[np.ix_(mask.any(1),mask.any(0))]

def main():
    sd = ShapeDetector()
    # Constallation Object
    cd = ConstellationBuilder()
    file = sys.argv[1]
    ursa_major = cd.build_ursa_major()
    constellations = cd.build_all()
    for constellation in constellations:
        fig, ax = plt.subplots()
        plt.scatter(constellation.stars_x, constellation.stars_y)
        # plt.axis([0, 8, -5, 0])
        for i, txt in enumerate(constellation.stars_mags):
            ax.annotate(txt, (constellation.stars_x[i], constellation.stars_y[i]))

        for line in constellation.lines:
            plt.plot((line.item(0), line.item(2)), (-line.item(1), -line.item(3)), 'ro-', linewidth=2, markersize=0)

        plt.show()

    # Read in Image
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    final_img = cv2.imread(file, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Starting Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #Threshold to binary
    thresh = 100
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    stars = sd.get_all(img)
    x,y,mags = sd.detect_stars(stars)
    fig, ax = plt.subplots()
    plt.scatter(x, y)
    for i, txt in enumerate(mags):
        ax.annotate(2*txt, (x[i], y[i]))

    #Find two brightest stars in image and mark them
    cd = ConstellationDetector(constellations)
    sorted_mags = order_mags(mags)
    l1, l2 = sorted_mags[0], sorted_mags[1]
    x_test = x.copy()
    y_test = y.copy()
    mags_test = mags.copy()
    for j in range(0, len(mags)):
        for constellation in constellations:
            for i in range(j, len(mags) - 1):
                tx, ty, lines, t_scale, matched = cd.search_for_constellation(constellation, x_test, y_test, mags_test, sorted_mags[j], sorted_mags[i])
                if matched:
                    break
            if matched:
                break
        if matched:
            break

    plt.plot(x_test[l1], y_test[l1], 'r+')
    plt.plot(x_test[l2], y_test[l2], 'y+')

    if matched:
        plt.plot(tx, ty, 'y*')
        for line in lines:
            plt.plot((line.item(0), line.item(2)), (-line.item(1), -line.item(3)), 'ro-', linewidth=2, markersize=0)
        # Draw constellation on image
        draw_stars(tx, ty, t_scale, final_img)
        draw_lines(lines, final_img)

    plt.show()

    height, width, channels = img.shape

    final_img = cv2.resize(final_img, (width*2, height*2))

    cv2.imshow('Finished Product', final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: python3 main.py {path to image}')
        exit()
    main()
