import numpy as np
import cv2

import Main
import EditFrame

def detectPlatesInScene(imgOriginalScene):
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
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    return