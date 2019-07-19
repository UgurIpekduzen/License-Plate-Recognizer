import cv2
import math

###################################################################################################
class PossibleChar:

    # constructor #################################################################################
    def __init__(self, _contour):
        self.contour = _contour

        self.boundRect = cv2.boundingRect(self.contour)

        [X, Y, width, height] = self.boundRect

        self.RectX = X
        self.RectY = Y
        self.RectWidth = width
        self.RectHeight = height

        self.RectArea = self.RectWidth * self.RectHeight

        self.CenterX = (self.RectX + self.RectX + self.RectWidth) / 2
        self.CenterY = (self.RectY + self.RectY + self.RectHeight) / 2

        self.fltDiagonalSize = math.sqrt((self.RectWidth ** 2) + (self.RectHeight ** 2))

        self.fltAspectRatio = float(self.RectWidth) / float(self.RectHeight)
    # end constructor

# end class
