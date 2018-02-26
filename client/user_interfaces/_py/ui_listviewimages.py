# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_listviewimages.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ListViewWindow(object):
    def setupUi(self, ListViewWindow):
        ListViewWindow.setObjectName("ListViewWindow")
        ListViewWindow.resize(942, 600)
        self.centralwidget = QtWidgets.QWidget(ListViewWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 921, 551))
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listWidget.setLineWidth(1)
        self.listWidget.setMidLineWidth(0)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.SelectedClicked)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.listWidget.setAlternatingRowColors(False)
        self.listWidget.setIconSize(QtCore.QSize(150, 150))
        self.listWidget.setMovement(QtWidgets.QListView.Snap)
        self.listWidget.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget.setProperty("isWrapping", True)
        self.listWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.listWidget.setLayoutMode(QtWidgets.QListView.Batched)
        self.listWidget.setGridSize(QtCore.QSize(200, 200))
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setModelColumn(0)
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setBatchSize(100)
        self.listWidget.setWordWrap(False)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setObjectName("listWidget")
        ListViewWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ListViewWindow)
        self.statusbar.setObjectName("statusbar")
        ListViewWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ListViewWindow)
        self.listWidget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(ListViewWindow)

    def retranslateUi(self, ListViewWindow):
        _translate = QtCore.QCoreApplication.translate
        ListViewWindow.setWindowTitle(_translate("ListViewWindow", "Система подбора причесок - просмотр результатов"))
        self.listWidget.setSortingEnabled(False)

