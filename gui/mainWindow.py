import sys
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/read_and edit_images")
import SQLQueries
import ReadImage
from time import time, sleep
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import cv2

from mainWindowUI import Ui_LPR_App

framePath = "E:/Repos/License-Plate-Recognizer-GitHub/gui/frames/"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LPR_App()
        self.ui.setupUi(self)
        self.LP = ""
        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.videoCaptureStream)
        self.timer.start(0)

        self.ui.ButtonStartReading.clicked.connect(self.readLicensePlateFromWebCam)
        self.ui.ButtonQueryVehicleInfoInDB.clicked.connect(self.getVehicleInfoFromDatabase)

        self.ui.LabelRegisteredIcon.setPixmap(QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/registered.png"))
        self.ui.LabelUnrecognizedIcon.setPixmap(QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/unknown.png"))
        self.ui.LabelBlackListedIcon.setPixmap(QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/blacklisted.png"))
        self.ui.LabelGuestIcon.setPixmap(QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/guest.png"))

    def videoCaptureStream(self):
        _, image = self.cap.read()
        imgReColoredImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = imgReColoredImage.shape
        step = channel * width
        qImg = QImage(imgReColoredImage.data, width, height, step, QImage.Format_RGB888)
        self.ui.LabelWebcamFrame.setPixmap(QPixmap.fromImage(qImg))

        # elapsedTime = int(time() % 60)
        # dateTime = str(datetime.now().strftime("%d%m%Y-%H%M%S"))
        # strFullPath = ''.join([framePath, dateTime, ".jpg"])
        # if elapsedTime % 3 == 0:
        #     cv2.imwrite(strFullPath, image)

        return image

    def updateGroupBoxMatchingVehicleInfoLabels(self, vehicle=None):
        if vehicle is None:
            self.ui.LabelLPText.setText("")
            self.ui.LabelRegisterStatusText.setText("")
            self.ui.LabelBLStatusText.setText("")
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap())
            self.ui.LabelNotificationMesssage.setText("")
        else:
            self.ui.LabelLPText.setText(vehicle[0][0])
            self.ui.LabelRegisterStatusText.setText("Evet" if vehicle[0][1] == 1 else "Hayır")
            self.ui.LabelBLStatusText.setText("Evet" if vehicle[0][1] == 1 else "Hayır")

    def setPassIcons(self):
        self.ui.LabelRegisteredIcon.setPixmap(
            QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/registered.png"))
        self.ui.LabelUnrecognizedIcon.setPixmap(
            QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/unknown.png"))
        self.ui.LabelBlackListedIcon.setPixmap(
            QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/blacklisted.png"))
        self.ui.LabelGuestIcon.setPixmap(QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/guest.png"))

    def readLicensePlateFromWebCam(self):
        self.updateGroupBoxMatchingVehicleInfoLabels()
        self.ui.LabelReadingLPText.setText("")
        self.ui.LabelReadingLPIcon.setPixmap(QPixmap())
        intCountdown = 10
        while True:
            self.LP = ReadImage.fromWebCamFrame(self.videoCaptureStream())
            if self.LP:
                self.ui.LabelReadingLPIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked.png"))
                self.ui.LabelReadingLPText.setText(self.LP)
                break
            else:
                if intCountdown == 0:
                    self.ui.LabelReadingLPIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel.png"))
                    self.ui.LabelReadingLPText.setText("PLAKA YOK")
                    break
                else:
                    intCountdown -= 1
                    self.ui.ProgressBarReadingCountdown.setProperty("value", intCountdown * 10)
                    sleep(1)
                # end if else
            # end if else
        # end while

    def getVehicleInfoFromDatabase(self):
        foundVehicle = SQLQueries.selectByLicensePlate(self.LP)
        if foundVehicle:
            self.updateGroupBoxMatchingVehicleInfoLabels(foundVehicle)
            self.ui.LabelRegisterStatusText.setText("Evet" if foundVehicle[0][1] == 1 else "Hayır")
            self.ui.LabelBLStatusText.setText("Evet" if foundVehicle[0][2] == 1 else "Hayır")

            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked2.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşen bir kayıt bulundu!")
        else:
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel2.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşen herhangi bir kayıt bulunamadı!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())