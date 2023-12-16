import os

import cv2
import subprocess

from paddleocr import PaddleOCR,draw_ocr
import easyocr

class OCRSingleton:
    instance = None
    def __init__(self):
        self._OCR = easyocr.Reader(['ch_tra'])

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
            if line[2] > 0.5:
                positionRect = line[0]
                center = ((positionRect[0][0] + positionRect[1][0]) / 2,
                          (positionRect[1][1] + positionRect[2][1]) / 2)
                lineList.append((line[1], center))
        return lineList

class PaddleOCRSingleton:
    instance = None
    def __init__(self):
        self._paddleOCR = PaddleOCR(lang="tw")

    @staticmethod
    def getInstance():
        if PaddleOCRSingleton.instance is None:
            PaddleOCRSingleton.instance = PaddleOCRSingleton()
        return PaddleOCRSingleton.instance

    def findTextPosition(self, img, text):
        result = self._paddleOCR.ocr(img, cls=False)
        for line in result[0]:
            # print(line)
            if text in line[1][0]:
                return (line[1][0], [(line[0][2][0] + line[0][3][0])/2, (line[0][1][1] + line[0][2][1])/2])
        return None

    def scanText(self, img):
        result = self._paddleOCR.ocr(img, cls=False)
        lineList = []
        for line in result[0]:
            # print(line)
            lineList.append((line[1][0], [(line[0][2][0] + line[0][3][0])/2, (line[0][1][1] + line[0][2][1])/2]))
        return lineList
