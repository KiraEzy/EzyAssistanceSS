import os

import cv2
import subprocess

import easyocr

class OCRSingleton:
    instance = None
    def __init__(self):
        self._OCR = easyocr.Reader(['ch_tra', 'en'])

    @staticmethod
    def getInstance():
        if OCRSingleton.instance is None:
            OCRSingleton.instance = OCRSingleton()
        return OCRSingleton.instance

    def findTextPosition(self, img, text):

        # Perform OCR on the image
        result = self._OCR.readtext(img)
        for line in result:
            # print(line)
            if line[2] > 0.3:
                if text in line[1]:
                    positionRect = line[0]
                    center = ((positionRect[0][0] + positionRect[1][0]) / 2,
                              (positionRect[1][1] + positionRect[2][1]) / 2)
                    return (line[1], center)
        return None

    def scanText(self, img):
        result = self._OCR.readtext(img)
        lineList = []
        for line in result:
            # print(line)
            if line[2] > 0.3:
                positionRect = line[0]
                center = ((positionRect[0][0] + positionRect[1][0]) / 2,
                          (positionRect[1][1] + positionRect[2][1]) / 2)
                lineList.append((line[1], center))
        return lineList

