# Main.py

import cv2
import numpy as np
from xlwt import Workbook


url = "https://10.0.10.51:8080/shot.jpg"

import DetectChars
import DetectPlates

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################

import urllib.request as urlreq
import os, ssl

PYTHONHTTPVERIFY = 0
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context

#####################################################################################################

def main():
    isClassificationFileExists = os.path.isfile("./classifications.txt")
    isFlattenedImagesFileExists = os.path.isfile("./flattened_images.txt")
    if (isClassificationFileExists and isFlattenedImagesFileExists) is False:
        isDataGenerated = DetectChars.generateData('E:/Repos/License Plate Recognizer/train20X20')
        if isDataGenerated == False:
            print("\nerror: generating data was not successful\n")  # show error message
            return  # and exit program
        #end if
    #end if
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN training was not successful\n")  # show error message
        return  # and exit program
    # end if

    # fromIPCAM()
    #fromLocalPath('E:/Repos/License Plate Recognizer/testimages/23.png')
    fromLPDatasetAndSaveXLS("E:/Repos/License Plate Recognizer/LPs")

    cv2.waitKey(0)  # hold windows open until user presses a key
    return
# end main

####################################################################################################

def readLPImagePaths(strFolderPath):
    listLP = []
    for file in os.listdir(strFolderPath):
            # Mevcut dizin ve alt dizinlerdeki tüm bilgileri toplar
            strFilePath = os.path.join(strFolderPath, file)
            listLP.append(strFilePath)
            print(strFilePath)
    return listLP

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

            # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function

###################################################################################################

# HATALI ##########################################################################################
def fromIPCAM():
    while True:
        imgResp = urlreq.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        imgOriginalScene = cv2.imdecode(imgNp, -1)
        cv2.imshow('AndroidCam', imgOriginalScene)

        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

        if len(listOfPossiblePlates) == 0:  # if no plates were found
            print("\nno license plates were detected\n")  # inform user no plates were found
        else:  # else
            # if we get in here list of possible plates has at leat one plate

            # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                print("\nno characters were detected\n\n")  # show message
            # end if

            print(
                "\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
            print("----------------------------------------")

        # end if else

        cv2.waitKey(0)  # hold windows open until user presses a key
    #end while
#end function

def fromLPDatasetAndSaveXLS(path):
    wb = Workbook()
    sheet = wb.add_sheet("Sheet 1")
    intXLSCounter = 0
    strDetectedLP = ""
    listlicensePlateSamples = readLPImagePaths(path)

    for imgLP in listlicensePlateSamples:
        imgOriginalScene = cv2.imread(imgLP)  # open image
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

        if len(listOfPossiblePlates) == 0:  # if no plates were found
            print("\nno license plates were detected\n")  # inform user no plates were found
            strDetectedLP = "OKUNMADI"
        else:  # else
            # if we get in here list of possible plates has at leat one plate

            # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                licPlate.strChars = "OKUNMADI"

            strDetectedLP = licPlate.strChars
        sheet.write(intXLSCounter, 0, imgLP)
        sheet.write(intXLSCounter, 1, strDetectedLP)
        intXLSCounter += 1
    # end for
    wb.save('results.xls')
#end function

def fromLocalPath(path):
    imgOriginalScene = cv2.imread(path)  # open image

    if imgOriginalScene is None:  # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")  # pause so user can see error message
        return  # and exit program
    # end if
    imgOriginalScene = adjust(imgOriginalScene,400)
    cv2.imshow("adjust", imgOriginalScene)
    cv2.waitKey(0)
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    cv2.imshow("imgOriginalScene", imgOriginalScene)  # show scene image

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:  # else
        # if we get in here list of possible plates has at leat one plate

        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate and threshold of plate
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:  # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return  # and exit program
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)  # draw red rectangle around plate

        print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
        print("----------------------------------------")

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)  # write license plate text on the image

        cv2.imshow("imgOriginalScene", imgOriginalScene)  # re-show scene image

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)  # write image out to file

    # end if else
#end function

#########################################################################################################################
def adjust(square, percent = 75):
    width = int(square.shape[1] * percent / 100)
    height = int(square.shape[0] * percent / 100)
    size = (width, height)
    return cv2.resize(square, size, interpolation= cv2.INTER_AREA)
# end function

if __name__ == "__main__":
    main()





















