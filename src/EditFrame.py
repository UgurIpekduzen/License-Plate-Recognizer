import cv2
import numpy as np
import Main
import os
###################################################################################################
def preprocess(imgOriginal):
    imgGrayscale = extractValue(imgOriginal)

# end function

###################################################################################################
def extractValue(imgOriginal):
    height, width, numChannels = imgOriginal.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    if Main.showSteps == True:
        cv2.imshow("H", imgHue)
        cv2.imshow("S", imgSaturation)
        cv2.imshow("V", imgValue)
        # cv2.imshow("Merge", cv2.merge((imgHue, imgSaturation, imgValue)))
        cv2.waitKey(0)

    return imgValue
# end function

###################################################################################################