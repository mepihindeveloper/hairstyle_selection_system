# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_initialization.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Initialization(object):
    def setupUi(self, Initialization):
        Initialization.setObjectName("Initialization")
        Initialization.resize(361, 575)
        self.centralwidget = QtWidgets.QWidget(Initialization)
        self.centralwidget.setObjectName("centralwidget")
        self.ui_Image = QtWidgets.QLabel(self.centralwidget)
        self.ui_Image.setGeometry(QtCore.QRect(10, 10, 341, 400))
        self.ui_Image.setObjectName("ui_Image")
        self.ui_HairType = QtWidgets.QComboBox(self.centralwidget)
        self.ui_HairType.setGeometry(QtCore.QRect(180, 420, 171, 41))
        self.ui_HairType.setObjectName("ui_HairType")
        self.ui_HairType.addItem("")
        self.ui_HairType.addItem("")
        self.ui_HairType.addItem("")
        self.ui_HairType.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 420, 161, 41))
        self.label_2.setObjectName("label_2")
        self.ui_SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.ui_SaveButton.setGeometry(QtCore.QRect(10, 510, 341, 31))
        self.ui_SaveButton.setObjectName("ui_SaveButton")
        Initialization.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Initialization)
        self.statusbar.setObjectName("statusbar")
        Initialization.setStatusBar(self.statusbar)

        self.retranslateUi(Initialization)
        QtCore.QMetaObject.connectSlotsByName(Initialization)

    def retranslateUi(self, Initialization):
        _translate = QtCore.QCoreApplication.translate
        Initialization.setWindowTitle(_translate("Initialization", "Администрирование - Настройка фотографий"))
        self.ui_Image.setText(_translate("Initialization", "TextLabel"))
        self.ui_HairType.setItemText(0, _translate("Initialization", "Нормальные"))
        self.ui_HairType.setItemText(1, _translate("Initialization", "Жирные"))
        self.ui_HairType.setItemText(2, _translate("Initialization", "Сухие"))
        self.ui_HairType.setItemText(3, _translate("Initialization", "Смешанные"))
        self.label_2.setText(_translate("Initialization", "Укажите тип волос"))
        self.ui_SaveButton.setText(_translate("Initialization", "Сохранить настройки"))

