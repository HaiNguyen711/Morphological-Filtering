import string
import cv2
from matplotlib import pyplot as mp
import numpy as np
from PIL import Image
from pandas import array

class Process:
    def __init__(self, path: string):
        self.baseImage = path 
        self.imgPIL = Image.open(self.baseImage)

    def initResultImage(self):
        self.convertImage = Image.new(self.imgPIL.mode, self.imgPIL.size)
        self.widthImage = self.convertImage.size[0]
        self.heightImage = self.convertImage.size[1]

    def Average(self, lst: list): 
        return sum(lst) / len(lst)

    def lgbToBinary(self):
        self.initResultImage()

        grayArray = []
        grayindexArray = []

        for x in range(self.widthImage):
            for y in range(self.heightImage):
                try:
                    R, G, B = self.imgPIL.getpixel((x, y)) 
                except:
                    R, G, B, L = self.imgPIL.getpixel((x, y)) 
                grayIndex = np.uint8((R + G + B) / 3) 
                grayindexArray.append(grayIndex) 
                grayArray.append([x, y, grayIndex]) 
      
        T = 100

        obj = []
        bgd = []
        self.temp = []

        for y in range(3):
            for x in grayindexArray:
                bgd.append(x) if x < T else obj.append(x) 
            T = (self.Average(obj) + self.Average(bgd)) / 2 

        for x in range(len(grayArray)):
            if (grayArray[x][2] < T ):
                self.convertImage.putpixel((grayArray[x][0],grayArray[x][1]), (0, 0, 0, 1))
                self.temp.append([grayArray[x][0], grayArray[x][1], 0])
            else: 
                self.convertImage.putpixel((grayArray[x][0],grayArray[x][1]), (255, 255, 255, 1)) 
                self.temp.append([grayArray[x][0], grayArray[x][1], 1])
        return np.array(self.convertImage)

    def dilate(self, kernel, new = True):
        if(new):
            self.lgbToBinary()
        for x in range(len(self.temp)):
            for y in range (1, kernel[0]):
                for z in range(1, kernel[1]):
                    if(self.temp[x][2] == 1):
                        if((self.temp[x][0]+z < self.widthImage) and (self.temp[x][1]+y < self.heightImage)):
                            self.convertImage.putpixel((self.temp[x][0]+z, self.temp[x][1]+y), (255, 255, 255, 1))
        return np.array(self.convertImage)

    def erode(self, kernel: array, new = True):
        if(new):
            self.lgbToBinary()
        for x in range(len(self.temp)):
            for y in range (1, kernel[0]):
                for z in range(1, kernel[1]):
                    if(self.temp[x][2] == 0):
                        if((self.temp[x][0]+z < self.widthImage) and (self.temp[x][1]+y < self.heightImage)):
                            self.convertImage.putpixel((self.temp[x][0]+z, self.temp[x][1]+y), (0, 0, 0, 1))
        return np.array(self.convertImage)

    def openning(self, kernel):
        self.dilate(kernel)
        self.erode(kernel, False)
        return np.array(self.convertImage)

    def closing(self, kernel):
        self.erode(kernel)
        self.dilate(kernel, False)
        return np.array(self.convertImage)



image = Process('data\logo-mu-inkythuatso-3-01-05-15-53-03.jpg')

x =3
kernel = [x,x]

cv2.imshow('Binary', image.lgbToBinary())
cv2.imshow('Erosion', image.erode(kernel))
cv2.imshow('Dilation', image.dilate(kernel))
cv2.imshow('Opening', image.openning(kernel))
cv2.imshow('Closing', image.closing(kernel))

cv2.waitKey(0)
cv2.destroyAllWindows()
mp.show()   