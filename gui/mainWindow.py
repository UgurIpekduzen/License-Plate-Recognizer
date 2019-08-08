import sys
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/read_and edit_images")
import SQLQueries
import ReadImage
import qtawesome as qta

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
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.LabelWebcamFrame.setPixmap(QPixmap.fromImage(qImg))

    def setPassIcons(self):
        self.ui.LabelRegisteredIcon.setPixmap(
            QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/registered.png"))
        self.ui.LabelUnrecognizedIcon.setPixmap(
            QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/unknown.png"))
        self.ui.LabelBlackListedIcon.setPixmap(
            QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/blacklisted.png"))
        self.ui.LabelGuestIcon.setPixmap(QPixmap("E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/guest.png"))

    def readLicensePlateFromWebCam(self):
        self.ui.LabelReadingLPText.setText("")
        # self.ui.MatchingVehicleInfoTextBrowser.setText("")
        self.LP = ReadImage.fromWebCam()
        if len(self.LP) > 0:
            self.ui.LabelReadingLPIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked.png"))
        else:
            self.ui.LabelReadingLPIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel.png"))
        self.ui.LabelReadingLPText.setText(self.LP)

    def getVehicleInfoFromDatabase(self):
        foundVehicle = SQLQueries.selectByLicensePlate(self.LP)
        self.ui.LabelLPText.setText("PLAKA")
        if(foundVehicle):
            self.ui.LabelLPText.setText(foundVehicle[0][0])
            self.ui.LabelRegisterStatusText.setText("Evet" if foundVehicle[0][1] == 1 else "Hayır")
            self.ui.LabelBLStatusText.setText("Evet" if foundVehicle[0][2] == 1 else "Hayır")

            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked2.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşen bir kayıt bulundu!")
        else:
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel2.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşen herhangi bir kayıt bulunamadı!")
        self.LP = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())