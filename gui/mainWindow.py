import sys
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/read_and edit_images")
import SQLQueries
import ReadImage

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from mainWindowUI import Ui_LPR_App

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LPR_App()
        self.ui.setupUi(self)
        self.ui.StartReadingButton.clicked.connect(self.readLicensePlateFromWebCam)
        self.ui.MatchingVehicleInfoPushButton.clicked.connect(self.loadClicked)
        self.LP = ""

    def readLicensePlateFromWebCam(self):
        self.LP = ReadImage.fromWebCam()
        self.ui.ReadingLPTextBrowser.setText(self.LP)
    def loadClicked(self):
        self.ui.MatchingVehicleInfoTextBrowser.setText(SQLQueries.showFoundVehicleDBInfo(self.LP))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())