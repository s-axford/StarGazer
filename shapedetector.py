# import the necessary packages
import cv2
import numpy as np
#include <math.h>
 
class ShapeDetector:
 
    #Returns mask of the stars in the image
    #img - Image to find stars in
    def get_stars(self, img):
        stars = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return cv2.inRange(stars, (240, 0, 0), (255, 10, 10))

    #Returns mask of lines in the image
    #img - image to find lines in
    def get_lines(self, img):
        lines = self.remove_stars(img)
        return cv2.inRange(lines, (1, 0, 0), (255, 255, 255))

    #Finds all stars in an image and return their cordinates and size
    #img - image to get star locations from
    #TODO Make this return values in a set scale so images are consistant
    def detect_stars(self, img):
        stars = self.get_stars(img)

	    # initialize the shape name and approximate the contour
        ret,thresh = cv2.threshold(stars,127,255,1)

        contours,h = cv2.findContours(thresh,1,2)
        x = []
        y = []
        labels = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx) > 8: #if a star is found
                #Find x and y cords
                M = cv2.moments(cnt)
                x.append(int(M["m10"] / M["m00"]))
                y.append((int(M["m01"] / M["m00"]))*-1)
                labels.append(len(cnt))
        return x,y,labels

    #Removes all stars from an image and returns result
    #img - image stars should be removed from
    def remove_stars(self, img):
        final = img.copy()
        stars = self.get_stars(img)
        ret,thresh = cv2.threshold(stars,127,255,1)

        contours,h = cv2.findContours(thresh,1,2)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx) > 8: #if a star is found
                cv2.drawContours(final,[cnt],0,(0,0,0),-1)
        return final

    #Finds all lines in an image and return their line endpoints
    #img - image to get line locations from
    #TODO Make this return values in a set scale so images are consistant // Finish implimentation
    def detect_lines(self, img):
        lines = self.get_lines(img)
        line_vector = cv2.HoughLinesP(lines,rho = 1,theta = 1*np.pi/180,threshold = 40,minLineLength = 1,maxLineGap = 20)
        print(len(line_vector))
        # dilated = cv2.dilate(lines, np.ones((5, 5)))    
        return line_vector