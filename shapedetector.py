# import the necessary packages
import cv2
import numpy as np
 
class ShapeDetector:
 
    def detect(self, img):
        stars = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        stars = cv2.inRange(stars, (240, 0, 0), (255, 10, 10))

        cv2.imshow('Stars', stars)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

	    # initialize the shape name and approximate the contour
        ret,thresh = cv2.threshold(stars,127,255,1)

        contours,h = cv2.findContours(thresh,1,2)

        cv2.imshow('Star Thresholds', thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            print(len(approx))
            if len(approx) > 8:
                print("circle")
                cv2.drawContours(img,[cnt],0,(0,255,255),-1)

