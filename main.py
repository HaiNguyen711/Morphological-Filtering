import cv2
import numpy as np
from matplotlib import pyplot as plt


baseImage = "data\wolf-glimage.png"

img = cv2.imread(baseImage, cv2.IMREAD_GRAYSCALE)  
(thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

x = 4;

kernel = np.ones((x,x),np.uint8)

erosion = cv2.erode(im_bw,kernel,iterations = 1)
dilation = cv2.dilate(im_bw, kernel, iterations = 1)
opening = cv2.morphologyEx(im_bw, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(im_bw, cv2.MORPH_CLOSE, kernel)

numpy_horizontal = np.hstack((erosion, dilation, opening, closing))

cv2.imshow("Show", numpy_horizontal)
cv2.waitKey(0)
cv2.destroyAllWindows()