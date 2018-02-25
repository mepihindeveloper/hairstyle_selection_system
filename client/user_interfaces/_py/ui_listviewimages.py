# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_listviewimages.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ListViewWindow(object):
    def setupUi(self, ListViewWindow):
        ListViewWindow.setObjectName("ListViewWindow")
        ListViewWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ListViewWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 781, 551))
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidget.setMovement(QtWidgets.QListView.Snap)
        self.listWidget.setObjectName("listWidget")
        ListViewWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ListViewWindow)
        self.statusbar.setObjectName("statusbar")
        ListViewWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ListViewWindow)
        QtCore.QMetaObject.connectSlotsByName(ListViewWindow)

    def retranslateUi(self, ListViewWindow):
        _translate = QtCore.QCoreApplication.translate
        ListViewWindow.setWindowTitle(_translate("ListViewWindow", "MainWindow"))

