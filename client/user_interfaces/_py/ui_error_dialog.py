# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_error_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ErrorDialog(object):
    def setupUi(self, ErrorDialog):
        ErrorDialog.setObjectName("ErrorDialog")
        ErrorDialog.resize(400, 100)
        self.centralwidget = QtWidgets.QWidget(ErrorDialog)
        self.centralwidget.setObjectName("centralwidget")
        self.uielem_closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.uielem_closeButton.setGeometry(QtCore.QRect(162, 60, 75, 23))
        self.uielem_closeButton.setObjectName("uielem_closeButton")
        self.uielem_errorText = QtWidgets.QLabel(self.centralwidget)
        self.uielem_errorText.setGeometry(QtCore.QRect(30, 20, 341, 31))
        self.uielem_errorText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.uielem_errorText.setObjectName("uielem_errorText")
        ErrorDialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(ErrorDialog)
        QtCore.QMetaObject.connectSlotsByName(ErrorDialog)

    def retranslateUi(self, ErrorDialog):
        _translate = QtCore.QCoreApplication.translate
        ErrorDialog.setWindowTitle(_translate("ErrorDialog", "Ошибка!"))
        self.uielem_closeButton.setText(_translate("ErrorDialog", "Закрыть"))
        self.uielem_errorText.setText(_translate("ErrorDialog", "Текст ошибки"))

