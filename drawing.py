import cv2

# Draws yellows circles relevant stars
# img - img to be drawn onto
# x, y - cordinates of stars
def draw_stars(x, y, scale, img):
    for star_index in range(len(x)):
        cv2.circle(img, (int(round(x[star_index]*100)), -int(round(y[star_index]*100))), int(round(scale)), (0, 255, 255), -1)


def draw_lines(lines, image):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (int(round(x1*100)), int(round(y1*100))), (int(round(x2*100)), int(round(y2*100))),
                     (255, 255, 255), 1)
