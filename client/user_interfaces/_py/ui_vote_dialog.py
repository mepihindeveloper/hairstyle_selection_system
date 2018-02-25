# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vote_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VoteDialog(object):
    def setupUi(self, VoteDialog):
        VoteDialog.setObjectName("VoteDialog")
        VoteDialog.resize(460, 100)
        self.centralwidget = QtWidgets.QWidget(VoteDialog)
        self.centralwidget.setObjectName("centralwidget")
        self.uielem_message = QtWidgets.QLabel(self.centralwidget)
        self.uielem_message.setGeometry(QtCore.QRect(20, 20, 411, 30))
        self.uielem_message.setTextFormat(QtCore.Qt.AutoText)
        self.uielem_message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.uielem_message.setWordWrap(True)
        self.uielem_message.setObjectName("uielem_message")
        self.uielem_yesButton = QtWidgets.QPushButton(self.centralwidget)
        self.uielem_yesButton.setGeometry(QtCore.QRect(160, 60, 75, 23))
        self.uielem_yesButton.setObjectName("uielem_yesButton")
        self.uielem_noButton = QtWidgets.QPushButton(self.centralwidget)
        self.uielem_noButton.setGeometry(QtCore.QRect(240, 60, 75, 23))
        self.uielem_noButton.setObjectName("uielem_noButton")
        VoteDialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(VoteDialog)
        QtCore.QMetaObject.connectSlotsByName(VoteDialog)

    def retranslateUi(self, VoteDialog):
        _translate = QtCore.QCoreApplication.translate
        VoteDialog.setWindowTitle(_translate("VoteDialog", "Оцените работу программы"))
        self.uielem_message.setText(_translate("VoteDialog", "Прорамма завершила поиск фоторафий по вашим критериям. Как вы оцениваете работу программы?"))
        self.uielem_yesButton.setText(_translate("VoteDialog", "Хорошо"))
        self.uielem_noButton.setText(_translate("VoteDialog", "Плохо"))

