# import sys
# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
#
# class Example(QWidget):
#
#     def __init__(self):
#         super(Example, self).__init__()
#         self.initUI()
#
#     def initUI(self):
#         QToolTip.setFont(QFont('Test', 10))
#         self.setToolTip('This is a <b>QWidget</b> widget')
#
#         # Show  image
#         self.pic = QLabel(self)
#         self.pic.setGeometry(10, 10, 800, 800)
#         self.pic.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked.png"))
#
#         # Show button
#         btn = QPushButton('Button', self)
#         btn.setToolTip('This is a <b>QPushButton</b> widget')
#         btn.resize(btn.sizeHint())
#         btn.clicked.connect(self.fun)
#         btn.move(50, 50)
#
#
#         self.setGeometry(300, 300, 2000, 1500)
#         self.setWindowTitle('Tooltips')
#         self.show()
#
#     # Connect button to image updating
#     def fun(self):
#         self.pic.setPixmap(QPixmap( "E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel.png"))
#
# def main():
#
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
# from time import *
#
# def getElapsedTime(intSecond):
#     return time() % intSecond if type(intSecond) is float else int(time() % intSecond)
#
# print(str(getElapsedTime(1.0)))

# a = [(1,2),(1,4),(3,5),(5,7)]
#
# print(str([item for item in a if item[0] == 1 and item[1] == 2]))

# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# import sys
#
#
# class ImageWidget(QLabel):
#
#     def __init__(self, imagePath, parent):
#         super(ImageWidget, self).__init__(parent)
#         self.picture = QPixmap(imagePath)
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.drawPixmap(0, 0, self.picture)
#
#
# class TableWidget(QTableView):
#
#     def setImage(self, row, col, imagePath):
#         image = ImageWidget(imagePath, self)
#         self.setCellWidget(row, col, image)
#
# if __name__ == "__main__":
#     app = QApplication([])
#     tableWidget = TableWidget()
#     tableWidget.setImage(0, 1, "E:/Repos/License-Plate-Recognizer-GitHub/gui/icon/guest.png")
#     tableWidget.show()
#     sys.exit(app.exec_())

# from PyQt5.QtWidgets import *
# # from PyQt5.QtCore import *
# # from PyQt5.QtGui import *
# # import sys
# #
# # class Model(QAbstractTableModel):
# #     def __init__(self, parent=None, *args):
# #         QAbstractTableModel.__init__(self, parent, *args)
# #         self.images = ['icon/cancel.png','icon/cancel.png','icon/cancel.png']
# #
# #     def resizePixmap(self, mult):
# #         self.thumbSize=self.thumbSize*mult
# #         self.reset()
# #
# #     def flags(self, index):
# #         return Qt.ItemIsEnabled | Qt.ItemIsSelectable
# #
# #     def rowCount(self, parent):
# #         return len(self.images)
# #     def columnCount(self, parent):
# #         return 3
# #
# #     def data(self, index, role):
# #
# #         if not index.isValid(): return QVariant()
# #
# #         row=index.row()
# #
# #         if role == Qt.DecorationRole:
# #             image=self.images[row]
# #             pixmap = QPixmap(image)
# #
# #             return pixmap
# #
# #         return QVariant()
# #
# #     def setData(self, index, value, role=Qt.EditRole):
# #         if index.isValid():
# #             if role == Qt.EditRole:
# #                 row = index.row()
# #                 self.images[row]=value
# #                 return True
# #         return False
# #
# #
# # class MyWindow(QWidget):
# #     def __init__(self, *args):
# #         QWidget.__init__(self, *args)
# #
# #         self.tablemodel=Model(self)
# #
# #         self.tableviewA=QTableView()
# #         self.tableviewA.setModel(self.tablemodel)
# #
# #         layout = QVBoxLayout(self)
# #         layout.addWidget(self.tableviewA)
# #
# #         self.setLayout(layout)
# #
# #     def zoomIn(self, arg):
# #         self.tablemodel.resizePixmap(1.1)
# #         self.resizeView()
# #
# #     def zoomOut(self, arg):
# #         self.tablemodel.resizePixmap(0.9)
# #         self.resizeView()
# #
# #     def resizeView(self):
# #         self.tableviewA.resizeRowsToContents()
# #         self.tableviewA.resizeColumnsToContents()
# #
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     w = MyWindow()
# #     w.show()
# #     sys.exit(app.exec_())

''' pqt_tableview3.py
explore PyQT's QTableView Model
using QAbstractTableModel to present tabular data
allow table sorting by clicking on the header title
used the Anaconda package (comes with PyQt4) on OS X
(dns)
'''

# coding=utf-8

import operator  # used for sorting
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import time
import threading
from datetime import datetime


class MyWindow(QWidget):
    def __init__(self, dataList, *args):
        QWidget.__init__(self, *args)

        self.setGeometry(70, 150, 1326, 582)

        self.table_model = MyTableModel(self, dataList)
        self.table_view = QTableView()
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        # bind cell click to a method reference
        self.table_view.clicked.connect(self.selectRow)

        self.table_view.setModel(self.table_model)
        # enable sorting

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def update_model(self, datalist):
        self.table_model2 = MyTableModel(self, dataList)
        self.table_view.setModel(self.table_model2)
        self.table_view.update()

    def showSelection(self, item):
        cellContent = item.data()
        print(cellContent)  # test
        sf = "You clicked on {}".format(cellContent)
        # display in title bar for convenience
        self.setWindowTitle(sf)

    def selectRow(self, index):
        print("current row is %d", index.row())
        pass


class MyTableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """

    def __init__(self, parent, mylist, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = ['Geçiş Durumu', 'Plaka', 'Zaman']
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

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

if __name__ == '__main__':
    app = QApplication([])

    # dataList = [
    #     [QPixmap('icon/cancel.png'), "0", '058176'],
    #     [QPixmap('icon/blacklisted.png'), "0", '058176'],
    #     [QPixmap('icon/guest.png')," 0", '058176'],
    #     [QPixmap('icon/unknown.png')," 0", '058176'],
    #     [QPixmap('icon/registered.png')," 0", '058176'],
    #     [QPixmap('icon/icons8-find-user-male-96.png')," 0", '058176'],
    #     [QPixmap('icon/icons8-registration-96.png')," 0", '058176'],
    # ]

    dataList = []

    data = (QPixmap('icon/cancel.png'), "0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    data = (QPixmap('icon/blacklisted.png')," 0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    data = (QPixmap('icon/guest.png')," 0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    data = (QPixmap('icon/unknown.png')," 0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    data = (QPixmap('icon/registered.png')," 0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    data = (QPixmap('icon/icons8-find-user-male-96.png')," 0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    data = (QPixmap('icon/icons8-registration-96.png')," 0", datetime.now().strftime("%d/%m/%Y %H:%M"))
    dataList.append(data)

    win = MyWindow(dataList)
    win.show()
    app.exec_()