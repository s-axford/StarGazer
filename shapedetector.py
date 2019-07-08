# import the necessary packages
import cv2
import numpy as np
 
class ShapeDetector:
 
    def detect_stars(self, img):
        stars = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        stars = cv2.inRange(stars, (240, 0, 0), (255, 10, 10))

	    # initialize the shape name and approximate the contour
        ret,thresh = cv2.threshold(stars,127,255,1)

        contours,h = cv2.findContours(thresh,1,2)
        x = []
        y = []
        labels = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx) > 8:
                print("circle")
                M = cv2.moments(cnt)
                x.append(int(M["m10"] / M["m00"]))
                y.append(int(M["m01"] / M["m00"]))
                labels.append(len(cnt))
                cv2.drawContours(img,[cnt],0,(0,255,255),-1)
        return x,y,labels
