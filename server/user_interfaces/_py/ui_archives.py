# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_archives.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Archives(object):
    def setupUi(self, Archives):
        Archives.setObjectName("Archives")
        Archives.resize(480, 530)
        self.centralwidget = QtWidgets.QWidget(Archives)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 461, 421))
        self.listWidget.setObjectName("listWidget")
        self.ui_MakeCopy = QtWidgets.QPushButton(self.centralwidget)
        self.ui_MakeCopy.setGeometry(QtCore.QRect(10, 10, 131, 41))
        self.ui_MakeCopy.setObjectName("ui_MakeCopy")
        self.ui_ResetCopy = QtWidgets.QPushButton(self.centralwidget)
        self.ui_ResetCopy.setGeometry(QtCore.QRect(150, 10, 131, 41))
        self.ui_ResetCopy.setObjectName("ui_ResetCopy")
        Archives.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Archives)
        self.statusbar.setObjectName("statusbar")
        Archives.setStatusBar(self.statusbar)

        self.retranslateUi(Archives)
        QtCore.QMetaObject.connectSlotsByName(Archives)

    def retranslateUi(self, Archives):
        _translate = QtCore.QCoreApplication.translate
        Archives.setWindowTitle(_translate("Archives", "Администрирование - Резервные копии"))
        self.ui_MakeCopy.setText(_translate("Archives", "Сделать копию"))
        self.ui_ResetCopy.setText(_translate("Archives", "Восстановить"))

