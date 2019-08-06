import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('Test', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # Show  image
        self.pic = QLabel(self)
        self.pic.setGeometry(10, 10, 800, 800)
        self.pic.setPixmap(QPixmap("E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\checked.png"))

        # Show button 
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.fun)
        btn.move(50, 50)


        self.setGeometry(300, 300, 2000, 1500)
        self.setWindowTitle('Tooltips')
        self.show()

    # Connect button to image updating 
    def fun(self):
        self.pic.setPixmap(QPixmap( "E:\Repos\License-Plate-Recognizer-GitHub\gui\icon\cancel.png"))

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()