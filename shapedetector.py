# import the necessary packages
import cv2
import numpy as np
 
class ShapeDetector:
 
    def get_stars(self, img):
        stars = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return cv2.inRange(stars, (240, 0, 0), (255, 10, 10))

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

    def remove_stars(self, img):
        lines = img
        stars = self.get_stars(img)
        ret,thresh = cv2.threshold(stars,127,255,1)

        contours,h = cv2.findContours(thresh,1,2)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx) > 8: #if a star is found
                cv2.drawContours(lines,[cnt],0,(0,0,0),-1)
        return lines


    def detect_lines(self, img):
        lines = self.remove_stars(img)
        cv2.imshow('lines', lines)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # dilated = cv2.dilate(img, np.ones((5, 5)))
        #Threshold to binary
        # thresh = 100
        # threshold = cv2.threshold(rgb, thresh, 255, cv2.THRESH_BINARY)[1]   
        # cv2.imshow('threshold', threshold)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # rgb[threshold > 100] = 255      
        # lines = cv2.inRange(lines, (0, 0, 0), (255, 255, 255))
        # lines = cv2.subtract(rgb, stars)
        # cv2.imshow('threshold', rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # lines = cv2.inRange( rgb, (0, 0, 200), (40, 40, 255)) + cv2.inRange( rgb, (200, 200, 200), (255, 255, 255))
        cv2.imshow('lines', lines)
        cv2.waitKey(0)
        cv2.destroyAllWindows()