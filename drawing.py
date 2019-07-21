import cv2

# Draws yellows circles relevant stars
# img - img to be drawn onto
# x, y - cordinates of stars
def draw_stars(x, y, scale, img):
    print("SCALE:")
    print(scale)
    for star_index in range(len(x)):
        cv2.circle(img, (int(round(x[star_index]*100)), -int(round(y[star_index]*100))), int(round(scale)), (0, 255, 255), -1)