import sys
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/read_and edit_images")
import SQLQueries
import ReadImage

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import cv2

from mainWindowUI import Ui_LPR_App

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LPR_App()
        self.ui.setupUi(self)

        self.timer = QTimer()
        # self.timer.timeout.connect(self.viewCam)
        self.ui.StartReadingButton.clicked.connect(self.readLicensePlateFromWebCam)
        self.ui.MatchingVehicleInfoPushButton.clicked.connect(self.getVehicleInfoFromDatabase)

    def viewCam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.FrameLabel.setPixmap(QPixmap.fromImage(qImg))

    def readLicensePlateFromWebCam(self):
        self.LP = QText
        # # if timer is stopped
        # if not self.timer.isActive():
        #     # create video capture
        #     self.cap = cv2.VideoCapture(0)
        #     # start timer
        #     self.timer.start(20)
        #     self.LP = ReadImage.fromWebCam()
        #
        # else:
        #     self.ui.ReadingLPTextBrowser.setText(self.LP)
        #     # stop timer
        #     self.timer.stop()
        #     # release video capture
        #     self.cap.release()
        #     # update control_bt text

        self.LP = ReadImage.fromWebCam()
        if len(self.LP) > 0:
            self.ui.ReadingLPIconLabel.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked.png"))
        else:
            self.ui.ReadingLPIconLabel.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel.png"))
        #
        #
        self.ui.ReadingLPTextBrowser.setText(self.LP)
        # self.ui.ReadingLPIconLabel = self.pixMapImage


    def getVehicleInfoFromDatabase(self):
        self.ui.MatchingVehicleInfoTextBrowser.setText(SQLQueries.showFoundVehicleDBInfo(self.LP))
        self.LP = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())