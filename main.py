import cv2

def main():
    img = cv2.imread('DemoImages/big_dipper.jpg', cv2.IMREAD_GRAYSCALE)
    thresh = 127
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]  
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    