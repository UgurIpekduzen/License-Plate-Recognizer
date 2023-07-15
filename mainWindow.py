import sys

# sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
# sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/read_and edit_images")
from database import SQLQueries
from src.read_and_edit_images import ReadImage
from time import time, sleep
from datetime import datetime

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import cv2

from MainWindowUI import Ui_LPR_App

framePath = "./frames"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LPR_App()
        self.ui.setupUi(self)
        self.selectedLicensePlate = ""
        self.arrayPreviousPlates = []
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.videoCaptureStream)
        self.timer.start(0)

        self.setPassIcons()
        self.ui.TableViewPreviousPlates.clicked.connect(self.getVehicleInfoFromDatabase)

        self.ui.ButtonAddNewRegistry.clicked.connect(self.addNewRegistry)
        self.ui.ButtonAddAsVisitor.clicked.connect(self.addAsVisitor)
        self.ui.ButtonDeleteCurrentRegistry.clicked.connect(self.deleteCurrentRegistry)
        self.ui.ButtonAddToBlackList.clicked.connect(self.addToBlackList)

        self.setGroupBoxMatchingVehicleInfoButtonsVisibility()

    def setGroupBoxMatchingVehicleInfoButtonsVisibility(self, addNewRegistryBtn=False, addAsVisitorBtn=False,
                                                        deleteRegistryBtn=False, addBlackListBtn=False):
        self.ui.ButtonAddNewRegistry.setVisible(addNewRegistryBtn)
        self.ui.ButtonAddAsVisitor.setVisible(addAsVisitorBtn)
        self.ui.ButtonDeleteCurrentRegistry.setVisible(deleteRegistryBtn)
        self.ui.ButtonAddToBlackList.setVisible(addBlackListBtn)

    def setPassIconsByLicensePlateStatus(self, strLicensePlate):
        if SQLQueries.identifyVehicleStatusByLicensePlate(strLicensePlate) is 'U':
            return QIcon("./icon/pass_icons/unknown.png")
        elif SQLQueries.identifyVehicleStatusByLicensePlate(strLicensePlate) is 'G':
            return QIcon("./icon/pass_icons/guest.png")
        elif SQLQueries.identifyVehicleStatusByLicensePlate(strLicensePlate) is 'R':
            return QIcon("./icon/pass_icons/registered.png")
        elif SQLQueries.identifyVehicleStatusByLicensePlate(strLicensePlate) is 'B':
            return QIcon("./icon/pass_icons/blacklisted.png")

    def getElapsedTime(self, intSecond):
        return time() % intSecond if type(intSecond) is float else int(time() % intSecond)

    def addNewRegistry(self):
        if SQLQueries.selectByLicensePlate(self.selectedLicensePlate):
            SQLQueries.updateSelectedVehicleInfo(self.selectedLicensePlate, 1, 0)
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
                QPixmap("./icon/matching_registry/30x30/add_data_alt_30x30.png"))
        else:
            SQLQueries.insertNewLicensePlate(self.selectedLicensePlate, 1, 0)
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
                QPixmap("./icon/matching_registry/30x30/added_30x30.png"))
        self.ui.LabelNotificationMesssage.setText("Yeni kayıt ekleme başarılı!")
        self.updateGroupBoxMatchingVehicleInfoLabels()
        self.setGroupBoxMatchingVehicleInfoButtonsVisibility()

    def addAsVisitor(self):
        SQLQueries.insertNewLicensePlate(self.selectedLicensePlate, 0, 0)
        self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
            QPixmap("./icon/matching_registry/30x30/import_data.png"))
        self.ui.LabelNotificationMesssage.setText("Misafir ekleme başarılı!")
        self.updateGroupBoxMatchingVehicleInfoLabels()
        self.setGroupBoxMatchingVehicleInfoButtonsVisibility()

    def addToBlackList(self):
        SQLQueries.updateSelectedVehicleInfo(self.selectedLicensePlate, 1, 1)
        self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
            QPixmap("./icon/matching_registry/30x30/update_30x30.png"))
        self.ui.LabelNotificationMesssage.setText("Kara listeye alma başarılı!")
        self.updateGroupBoxMatchingVehicleInfoLabels()
        self.setGroupBoxMatchingVehicleInfoButtonsVisibility()

    def deleteCurrentRegistry(self):
        SQLQueries.deleteByLicensePlate(self.selectedLicensePlate)
        self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
            QPixmap("./icon/matching_registry/30x30/remove_data_30x30.png"))
        self.ui.LabelNotificationMesssage.setText("Kayıt silme başarılı!")
        self.updateGroupBoxMatchingVehicleInfoLabels()
        self.setGroupBoxMatchingVehicleInfoButtonsVisibility()

    def videoCaptureStream(self):
        _, image = self.cap.read()
        imgReColoredImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = imgReColoredImage.shape
        step = channel * width
        qImg = QImage(imgReColoredImage.data, width, height, step, QImage.Format.Format_RGB888)
        self.ui.LabelWebcamFrame.setPixmap(QPixmap.fromImage(qImg))

        if self.getElapsedTime(3) is 0:
            self.readLicensePlateFromWebCam(image)

    def updateGroupBoxMatchingVehicleInfoLabels(self, vehicle=None):
        if vehicle is None:
            self.ui.LabelLPText.setText("")
            self.ui.LabelRegisterStatusText.setText("")
            self.ui.LabelBLStatusText.setText("")
        else:
            self.ui.LabelLPText.setText(vehicle[0][0])
            self.ui.LabelRegisterStatusText.setText("Evet" if vehicle[0][1] is 1 else "Hayır")
            self.ui.LabelBLStatusText.setText("Evet" if vehicle[0][1] is 1 else "Hayır")

    def setPassIcons(self):
        self.ui.LabelRegisteredIcon.setPixmap(
            QPixmap("./icon/pass_icons/registered.png"))
        self.ui.LabelUnrecognizedIcon.setPixmap(
            QPixmap("./icon/pass_icons/unknown.png"))
        self.ui.LabelBlackListedIcon.setPixmap(
            QPixmap("./icon/pass_icons/blacklisted.png"))
        self.ui.LabelGuestIcon.setPixmap(
            QPixmap("./icon/pass_icons/guest.png"))

    def readLicensePlateFromWebCam(self, image):

        strReadLicensePlate = ReadImage.fromWebCamFrame(image)

        if self.getElapsedTime(3) is not 0:
            if strReadLicensePlate:
                self.ui.LabelReadingLPIcon.setPixmap(
                    QPixmap("./icon/reading_plates/checked.png"))
                self.ui.LabelReadingLPText.setText(strReadLicensePlate)

                arrayTupleElement = (self.setPassIconsByLicensePlateStatus(strReadLicensePlate),
                                     strReadLicensePlate,
                                     datetime.now().strftime("%d/%m/%Y %H:%M"))
                if len([item for item in self.arrayPreviousPlates if
                        (arrayTupleElement[1] in item and arrayTupleElement[2] in item)]) is 0:
                    self.arrayPreviousPlates.append(arrayTupleElement)
                    self.ui.TableViewPreviousPlates.setModel(MyTableModel(self, self.arrayPreviousPlates))
            else:
                self.ui.LabelReadingLPIcon.setPixmap(
                    QPixmap("./icon/reading_plates/cancel.png"))
                self.ui.LabelReadingLPText.setText("PLAKA YOK")
            # end if else
        else:
            self.ui.LabelReadingLPText.setText("")
            self.ui.LabelReadingLPIcon.setPixmap(QPixmap())
        # end if else

    def getVehicleInfoFromDatabase(self, item):
        self.selectedLicensePlate = self.arrayPreviousPlates[item.row()][1]
        foundVehicle = SQLQueries.selectByLicensePlate(self.selectedLicensePlate)
        if foundVehicle:
            self.ui.LabelLPText.setText(foundVehicle[0][0])
            self.ui.LabelRegisterStatusText.setText("Evet" if foundVehicle[0][1] is 1 else "Hayır")
            self.ui.LabelBLStatusText.setText("Evet" if foundVehicle[0][2] is 1 else "Hayır")
            self.setGroupBoxMatchingVehicleInfoButtonsVisibility(True if foundVehicle[0][1] is 0 else False,
                                                                 False,
                                                                 True if foundVehicle[0][1] is 1 else False,
                                                                 True if foundVehicle[0][1] is 1 and foundVehicle[0][2] is 0 else False)
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
                QPixmap("./icon/matching_registry/30x30/search_data_30x30.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşme başarılı!")
        else:
            self.ui.LabelLabelNotificationMesssageIcon.setPixmap(
                QPixmap("./icon/matching_registry/30x30/not_found_30x30.png"))
            self.ui.LabelNotificationMesssage.setText("Eşleşme bulunamadı!")
            self.setGroupBoxMatchingVehicleInfoButtonsVisibility(True, True, False, False)
        # end if else
    # end function
# end class

class MyTableModel(QAbstractTableModel):

    def __init__(self, parent, list, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = list
        self.header = ['DURUM', 'PLAKA', 'ZAMAN']
        self.change_flag = True

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        value = self.mylist[index.row()][index.column()]
        if not index.isValid():
            return None
        elif role == Qt.DisplayRole:
            return value
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                pixmap = self.mylist[index.row()][0]
                return pixmap
        return QVariant()

    def data(self, index, role):
        value = self.mylist[index.row()][index.column()]
        if not index.isValid():
            return None
        elif role == Qt.ItemDataRole.DisplayRole:
            return value
        elif role == Qt.ItemDataRole.DecorationRole:
            if index.column() == 0:
                pixmap = self.mylist[index.row()][0]
                return pixmap
        return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.header[col]
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
