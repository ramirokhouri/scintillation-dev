# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from S4count import SUMProcessor

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(self)
        self.button = QtGui.QPushButton('Select Files', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.handleButton)
        self.path_list = []

    def handleButton(self):
    	i = 1
    	title = self.button.text()
        
    	for path in QtGui.QFileDialog.getOpenFileNames(self, title):
            self.path_list.append(str(path))


        print self.path_list
        sum_processor = SUMProcessor(self.path_list)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())