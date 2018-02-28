# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_web_cam.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WebCamWindow(object):
    def setupUi(self, WebCamWindow):
        WebCamWindow.setObjectName("WebCamWindow")
        WebCamWindow.resize(640, 578)
        WebCamWindow.setMaximumSize(QtCore.QSize(640, 578))
        WebCamWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(WebCamWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ui_makePhoto = QtWidgets.QPushButton(self.centralwidget)
        self.ui_makePhoto.setGeometry(QtCore.QRect(240, 500, 151, 41))
        self.ui_makePhoto.setObjectName("ui_makePhoto")
        self.videoFrame = QtWidgets.QLabel(self.centralwidget)
        self.videoFrame.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.videoFrame.setMaximumSize(QtCore.QSize(640, 480))
        self.videoFrame.setObjectName("videoFrame")
        WebCamWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(WebCamWindow)
        self.statusbar.setObjectName("statusbar")
        WebCamWindow.setStatusBar(self.statusbar)

        self.retranslateUi(WebCamWindow)
        QtCore.QMetaObject.connectSlotsByName(WebCamWindow)

    def retranslateUi(self, WebCamWindow):
        _translate = QtCore.QCoreApplication.translate
        WebCamWindow.setWindowTitle(_translate("WebCamWindow", "Система подбора причесок - снимок клиента"))
        self.ui_makePhoto.setText(_translate("WebCamWindow", "Сделать снимок"))
        self.videoFrame.setText(_translate("WebCamWindow", "TextLabel"))

