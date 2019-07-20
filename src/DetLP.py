import numpy as np
import cv2
import random
import math

import Main
import EditFrame
import PossibleChar
import PossibleLP
import DetCh

# module level variables ##########################################################################
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5
###################################################################################################
def detectPlatesInFrame(imgOriginal):
    listPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginal.shape #yükseklik, genişlik, renk kanalları

    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("0", imgOriginal)
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    imgGrayscaleScene, imgThreshScene = EditFrame.preprocess(imgOriginal)         # preprocess to get grayscale and threshold images

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("grayscale", imgGrayscaleScene)
        cv2.imshow("threshold", imgThreshScene)
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    listPossibleCharsInFrame = findPossibleCharsInFrame(imgThreshScene)

    if Main.showSteps == True:  # show steps #######################################################
        print("step 2 - len(listOfPossibleCharsInScene) = " + str(
            len(listPossibleCharsInFrame)))

        imgContours = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in listPossibleCharsInFrame:
            contours.append(possibleChar.contour)
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("contours", imgContours)

        listOfListsOfMatchingChars = DetCh.findListOfListsOfMatchingChars(listPossibleCharsInFrame)

        if Main.showSteps == True:  # show steps #######################################################
            print("step 3 - listOfListsOfMatchingCharsInScene.Count = " + str(
                len(listOfListsOfMatchingChars)))
            cv2.waitKey(0)

            imgContours = np.zeros((height, width, 3), np.uint8)

            for listMatchingChars in listOfListsOfMatchingChars:
                intRandomBlue = random.randint(0, 255)
                intRandomGreen = random.randint(0, 255)
                intRandomRed = random.randint(0, 255)

                contours = []

                for matchingChar in listMatchingChars:
                    contours.append(matchingChar.contour)
                # end for

                cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for

            cv2.imshow("3", imgContours)
        # end if # show steps #########################################################################

        for listMatchingChars in listOfListsOfMatchingChars:  # for each group of matching chars
            possibleLP = extractPlate(imgOriginal, listMatchingChars)  # attempt to extract plate
            #Eğer plaka bulunursa olası plakaların listesine ekler
            if possibleLP.imgPlate is not None: # if plate was found
                listPossiblePlates.append(possibleLP) # add to list of possible plates
            # end if
        # end for

        print("\n" + str(len(listPossiblePlates)) + " possible plates found")

        if Main.showSteps == True:  # show steps #######################################################
            print("\n")
            cv2.imshow("4a", imgContours)

            for i in range(0, len(listPossiblePlates)):
                p2fRectPoints = cv2.boxPoints(listPossiblePlates[i].rrLocationOfPlateInScene)

                cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Main.SCALAR_RED, 2)
                cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Main.SCALAR_RED, 2)
                cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Main.SCALAR_RED, 2)
                cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Main.SCALAR_RED, 2)

                cv2.imshow("4a", imgContours)

                print("possible plate " + str(i) + ", click on any image and press a key to continue . . .")

                cv2.imshow("4b", listPossiblePlates[i].imgPlate)
                cv2.waitKey(0)
            # end for

            print("\nplate detection complete, click on any image and press a key to begin char recognition . . .\n")
            cv2.waitKey(0)
        # end if # show steps #########################################################################

        return listPossiblePlates
    return

def findPossibleCharsInFrame(imgThresh):
    listChars = []  # this will be the return value

    countChars = 0

    imgThreshCopy = imgThresh.copy()

    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find all contours

    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contours)):                       # for each contour

        if Main.showSteps == True: # show steps ###################################################
            cv2.drawContours(imgContours, contours, i, Main.SCALAR_WHITE)
        # end if # show steps #####################################################################

        possibleChar = PossibleChar.PossibleChar(contours[i])

        if DetCh.checkIfPossibleChar(possibleChar):                   # if contour is a possible char, note this does not compare to other chars (yet) . . .
            countChars = countChars + 1           # increment count of possible chars
            listChars.append(possibleChar)                        # and add to list of possible chars
        # end if
    # end for

        if Main.showSteps == True:  # show steps #######################################################
            print("\nstep 2 - len(contours) = " + str(len(contours)))
            print("step 2 - intCountOfPossibleChars = " + str(countChars))
            cv2.waitKey(0)
        # end if # show steps #########################################################################

        return listChars
    # end function

###################################################################################################
def extractPlate(imgOriginal, listOfMatchingChars):
    possibleLP = PossibleLP.PossibleLP()           # this will be the return value

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right based on x position

            # calculate the center point of the plate
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

            # calculate plate width and height
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

            # calculate correction angle of plate region
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetCh.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

            # pack plate region center point, width and height, and correction angle into rotated rect member variable of plate
    possibleLP.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

            # final steps are to perform the actual rotation

            # get the rotation matrix for our calculated correction angle
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape      # unpack original image width and height

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # rotate the entire image

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    possibleLP.imgPlate = imgCropped         # copy the cropped plate image into the applicable member variable of the possible plate

    return possibleLP
# end function