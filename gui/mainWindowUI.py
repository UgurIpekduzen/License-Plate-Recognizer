# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Repos\License-Plate-Recognizer-GitHub\gui\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LPR_App(object):
    def setupUi(self, LPR_App):
        LPR_App.setObjectName("LPR_App")
        LPR_App.resize(1440, 841)
        self.verticalLayoutWidget = QtWidgets.QWidget(LPR_App)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 621, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.WebCamStreamLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.WebCamStreamLayout.setContentsMargins(0, 0, 0, 0)
        self.WebCamStreamLayout.setObjectName("WebCamStreamLayout")
        self.WebCamStreamLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.WebCamStreamLabel.setObjectName("WebCamStreamLabel")
        self.WebCamStreamLayout.addWidget(self.WebCamStreamLabel)
        self.FrameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FrameLabel.setText("")
        self.FrameLabel.setObjectName("FrameLabel")
        self.WebCamStreamLayout.addWidget(self.FrameLabel)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(LPR_App)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 420, 621, 401))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.ProcessLogLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.ProcessLogLayout.setContentsMargins(0, 0, 0, 0)
        self.ProcessLogLayout.setObjectName("ProcessLogLayout")
        self.ProcessLogLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.ProcessLogLabel.setObjectName("ProcessLogLabel")
        self.ProcessLogLayout.addWidget(self.ProcessLogLabel)
        self.ProcessLogListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.ProcessLogListWidget.setObjectName("ProcessLogListWidget")
        self.ProcessLogLayout.addWidget(self.ProcessLogListWidget)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(LPR_App)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(780, 420, 641, 401))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.MatchingVehicleInfoLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.MatchingVehicleInfoLayout.setContentsMargins(0, 0, 0, 0)
        self.MatchingVehicleInfoLayout.setObjectName("MatchingVehicleInfoLayout")
        self.MatchingVehicleInfoLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.MatchingVehicleInfoLabel.setObjectName("MatchingVehicleInfoLabel")
        self.MatchingVehicleInfoLayout.addWidget(self.MatchingVehicleInfoLabel)
        self.MatchingVehicleInfoTextBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.MatchingVehicleInfoTextBrowser.setFont(font)
        self.MatchingVehicleInfoTextBrowser.setObjectName("MatchingVehicleInfoTextBrowser")
        self.MatchingVehicleInfoLayout.addWidget(self.MatchingVehicleInfoTextBrowser)
        self.MatchingVehicleInfoPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.MatchingVehicleInfoPushButton.setObjectName("MatchingVehicleInfoPushButton")
        self.MatchingVehicleInfoLayout.addWidget(self.MatchingVehicleInfoPushButton)
        self.ReadingLPTextLabel = QtWidgets.QLabel(LPR_App)
        self.ReadingLPTextLabel.setGeometry(QtCore.QRect(780, 10, 641, 20))
        self.ReadingLPTextLabel.setObjectName("ReadingLPTextLabel")
        self.ReadingLPTextBrowser = QtWidgets.QTextBrowser(LPR_App)
        self.ReadingLPTextBrowser.setGeometry(QtCore.QRect(930, 40, 481, 100))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.ReadingLPTextBrowser.setFont(font)
        self.ReadingLPTextBrowser.setObjectName("ReadingLPTextBrowser")
        self.ReadingLPIconLabel = QtWidgets.QLabel(LPR_App)
        self.ReadingLPIconLabel.setGeometry(QtCore.QRect(780, 40, 100, 100))
        self.ReadingLPIconLabel.setObjectName("ReadingLPIconLabel")
        self.StartReadingButton = QtWidgets.QPushButton(LPR_App)
        self.StartReadingButton.setGeometry(QtCore.QRect(780, 190, 631, 61))
        self.StartReadingButton.setObjectName("StartReadingButton")

        self.retranslateUi(LPR_App)
        QtCore.QMetaObject.connectSlotsByName(LPR_App)

    def retranslateUi(self, LPR_App):
        _translate = QtCore.QCoreApplication.translate
        LPR_App.setWindowTitle(_translate("LPR_App", "Form"))
        self.WebCamStreamLabel.setText(_translate("LPR_App", "Web Cam:"))
        self.ProcessLogLabel.setText(_translate("LPR_App", "İşlem Günlüğü:"))
        self.MatchingVehicleInfoLabel.setText(_translate("LPR_App", "Eşleşen Kayıt Bilgileri:"))
        self.MatchingVehicleInfoPushButton.setText(_translate("LPR_App", "Göster"))
        self.ReadingLPTextLabel.setText(_translate("LPR_App", "Okunan Plaka:"))
        self.ReadingLPTextBrowser.setHtml(_translate("LPR_App", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:50pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p></body></html>"))
        self.StartReadingButton.setText(_translate("LPR_App", "Başlat"))
