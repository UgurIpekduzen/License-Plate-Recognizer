import numpy as np
import cv2

import Main
import EditFrame
import PossibleChar
import DetCh

def detectPlatesInFrame(imgOriginalScene):
    listOfPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginalScene.shape #yükseklik, genişlik, renk kanalları

    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("0", imgOriginalScene)
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    imgGrayscaleScene, imgThreshScene = EditFrame.preprocess(imgOriginalScene)         # preprocess to get grayscale and threshold images

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("grayscale", imgGrayscaleScene)
        cv2.imshow("threshold", imgThreshScene)
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    listPossibleCharsInFrame = findPossibleCharsInFrame(imgThreshScene)

    if Main.showSteps == True:  # show steps #######################################################
        print("step 2 - len(listOfPossibleCharsInScene) = " + str(
            len(listPossibleCharsInFrame)))  # 131 with MCLRNF1 image

        imgContours = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in listPossibleCharsInFrame:
            contours.append(possibleChar.contour)
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("2b", imgContours)
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
