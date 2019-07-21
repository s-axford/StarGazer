# import the necessary packages
import cv2
import numpy as np


class ShapeDetector:

    def get_all(self, img):
        stars = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return cv2.inRange(stars, (0, 0, 1), (255, 255, 255))

    #  Returns mask of the stars in the image
    #  img - Image to find stars in
    def get_stars(self, img):
        stars = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return cv2.inRange(stars, (240, 0, 0), (255, 10, 10))

    #  Returns mask of lines in the image
    #  img - image to find lines in
    def get_lines(self, img):
        lines = self.remove_stars(img)
        return cv2.inRange(lines, (1, 0, 0), (255, 255, 255))

    #  Finds all stars in an image and return their cordinates and size
    #  img - image to get star locations from
    def detect_stars(self, stars):
        # initialize the shape name and approximate the contour
        ret, thresh = cv2.threshold(stars, 127, 255, 1)
        contours, h = cv2.findContours(thresh, 1, 2)

        x = []
        y = []
        labels = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if len(approx) > 2:  # if a star is found
                # Find x and y cords
                M = cv2.moments(cnt)
                x_star = (int(M["m10"] / M["m00"]))/100
                y_star = ((int(M["m01"] / M["m00"]))*-1)/100

                # Removing duplicates if multiple stars are found in one spot
                if x_star in x:
                    index = x.index(x_star)
                    if round(y_star, 1) == round(y[index], 1):
                        if len(cnt) < labels[index]:
                            labels[index] = len(cnt)
                        continue
                if y_star in y:
                    index = y.index(y_star)
                    if round(x_star, 1) == round(x[index], 1):
                        # adding label if smaller
                        a, b, w, h = cv2.boundingRect(cnt)
                        if min([w, h]) < labels[index] and cv2.contourArea(cnt) < 2000:
                            labels[index] = round(min([w, h]), 2)
                        continue

                # Remove middle dot
                if cv2.contourArea(cnt) < 2000:
                    x.append(x_star)
                    y.append(y_star)
                    # use smallest length of bounding rectangle as relative size
                    a, b, w, h = cv2.boundingRect(cnt)
                    labels.append(round(min([w, h]), 2))
        return x, y, labels

    # Removes all stars from an image and returns result
    # img - image stars should be removed from
    def remove_stars(self, img):
        final = img.copy()
        stars = self.get_stars(img)
        ret, thresh = cv2.threshold(stars, 127, 255, 1)

        contours, h = cv2.findContours(thresh, 1, 2)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt, True), True)
            if len(approx) > 8: # if a star is found
                cv2.drawContours(final, [cnt], 0, (0, 0, 0), -1)
        return final

    # Finds all lines in an image and return their line endpoints
    # img - image to get line locations from
    def detect_lines(self, img):
        lines = self.get_lines(img)
        line_vector = cv2.HoughLinesP(lines, rho=1, theta=np.pi/180, threshold=8, minLineLength=0, maxLineGap=30)

        # Convert int array to float to maintain shape after scaling
        new_line_vector = line_vector.astype(float)
        for i in range(len(new_line_vector)):
            for j in range(len(line_vector[i])):
                new_lines = np.zeros(4)
                for k in range(len(line_vector[i][j])):
                    x = np.float(line_vector[i][j][k])
                    # scale images to same size
                    new_lines[k] = x/100.0
                new_line_vector[i][j] = new_lines
        return new_line_vector

    def get_image_size(self, img):
        # initialize the shape name and approximate the contour
        ret, thresh = cv2.threshold(img, 255, 255, 1)
        contours, h = cv2.findContours(thresh, 1, 2)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if len(approx) > 0:  # if a star is found
                # Find x and y cords
                M = cv2.moments(cnt)
                x_star = (int(M["m10"] / M["m00"]))/100
                y_star = ((int(M["m01"] / M["m00"]))*-1)/100
                print(x_star)
                print(y_star)
                cv2.drawContours(img, [cnt], 0, (255, 255, 255), -1)