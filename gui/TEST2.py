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
        self.arrayPreviousPlates = []
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.videoCaptureStream)
        self.timer.start(0)

        self.setPassIcons()
        self.ui.tableViewPreviousPlates.clicked.connect(self.getVehicleInfoFromDatabase)

    def getElapsedTime(self,intSecond):
        return time() % intSecond if type(intSecond) is float else int(time() % intSecond)

    def videoCaptureStream(self):
        _, image = self.cap.read()
        imgReColoredImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = imgReColoredImage.shape
        step = channel * width
        qImg = QImage(imgReColoredImage.data, width, height, step, QImage.Format_RGB888)
        self.ui.LabelWebcamFrame.setPixmap(QPixmap.fromImage(qImg))

        if self.getElapsedTime(3) is 0:
            self.readLicensePlateFromWebCam(image)

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

    def readLicensePlateFromWebCam(self, image):

        self.LP = ReadImage.fromWebCamFrame(image)
        if self.getElapsedTime(4) is not 0:
            if self.LP:
                self.ui.LabelReadingLPIcon.setPixmap(
                    QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked.png"))
                self.ui.LabelReadingLPText.setText(self.LP)
                arrayTupleElement = ((QIcon("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked2.png"),
                                        self.LP,
                                        datetime.now().strftime("%d/%m/%Y %H:%M")))

                if len([item for item in self.arrayPreviousPlates if (arrayTupleElement[1] in item) and (arrayTupleElement[2] in item)]) is 0:
                    self.arrayPreviousPlates.append(arrayTupleElement)
                    self.ui.tableViewPreviousPlates.setModel(MyTableModel(self.arrayPreviousPlates, self))

            else:
                self.ui.LabelReadingLPIcon.setPixmap(
                    QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel.png"))
                self.ui.LabelReadingLPText.setText("PLAKA YOK")
            # end if else
        else:
            self.ui.LabelReadingLPText.setText("")
            self.ui.LabelReadingLPIcon.setPixmap(QPixmap())
        # end if else


    def getVehicleInfoFromDatabase(self, item):
        LP = item.data()
        foundVehicle = SQLQueries.selectByLicensePlate(LP)
        if foundVehicle:
            self.ui.LabelLPText.setText(foundVehicle[0][0])
            self.ui.LabelRegisterStatusText.setText("Evet" if foundVehicle[0][1] == 1 else "Hayır")
            self.ui.LabelBLStatusText.setText("Evet" if foundVehicle[0][2] == 1 else "Hayır")

            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked2.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşen bir kayıt bulundu!")
        else:
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel2.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşen herhangi bir kayıt bulunamadı!")
        # end if else
    # end function
# end class

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())