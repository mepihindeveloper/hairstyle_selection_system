import sys
import os
import cv2
import imutils
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore
from client.user_interfaces._py.ui_design import Ui_MainWindow
from client.user_interfaces._py.ui_vote_dialog import Ui_VoteDialog
from client.user_interfaces._py.ui_error_dialog import Ui_ErrorDialog
from client.user_interfaces._py.ui_listviewimages import Ui_ListViewWindow
from client.user_interfaces._py.ui_web_cam import Ui_WebCamWindow


'''
    Класс ErrorWin описвает отображение окна с ошибкой
'''


class ErrorWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, error_message=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self)

        self.ui.uielem_closeButton.clicked.connect(self.close_win)

        # Назначаем текст ошибки
        self.ui.uielem_errorText.setText(error_message)

    def close_win(self):
        self.close()


'''
    Класс VoteWin описывает работу диалога по голосованию за результат программы
'''


class VoteWin(QtWidgets.QMainWindow):
    server_class = None

    def __init__(self, parent=None, server_class=None):
        self.server_class = server_class

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_VoteDialog()
        self.ui.setupUi(self)

        # События нажатия на кнопки: "Хорошо" и "Плохо"
        self.ui.uielem_yesButton.clicked.connect(self.vote_yes)
        self.ui.uielem_noButton.clicked.connect(self.vote_no)


    # Функция голосования за положительный резуальтат работы программы
    def vote_yes(self):
        result = self.server_class.set_rating()
        self.ui.uielem_message.setText(result.get("message"))
        self.init_timer()

    # Функця для задержки перед закрытием окна
    def init_timer(self):
        timer = QtCore.QTimer(self)
        timer.setInterval(3000)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.close())
        timer.start()

    # Функция голосования за отрицательный резуальтат работы программы
    def vote_no(self):
        result = self.server_class.set_rating('negative')
        self.ui.uielem_message.setText(result.get("message"))
        self.init_timer()


'''
    Класс MainWin описывает окно и событие UI (интерфейс пользователя) элементов
    Необходим для показа и работы UI
'''


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, server_class=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.server_class = server_class
        self.params = {
            'hair_type': 'normal',
            'hair_length': 'short',
            'hair_color': 'Red',
            'gender': 'women'
        }

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())

        # Блок для нормализации вида таблицы
        self.ui.ui_hairTypeDescriptionTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.ui.ui_hairTypeDescriptionTable.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )
        self.ui.ui_hairTypeDescriptionTable.resizeRowsToContents()
        self.ui.ui_hairTypeDescriptionTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        # Привязка функкции смены цвета
        self.ui.ui_hairColorComboBox.currentIndexChanged.connect(self.change_color)
        # Привязка функкции смены типа волос
        self.ui.ui_hairTypeComboBox.currentIndexChanged.connect(self.change_hair_type)
        # Привязка функкции смены длины волос
        self.ui.ui_hairLengthComboBox.currentIndexChanged.connect(self.change_hair_length)
        # Привязка функции к смене пола
        self.ui.radioButton.toggled.connect(
            lambda: self.change_gender(self.ui.radioButton,"men")
        )
        self.ui.radioButton_2.toggled.connect(
            lambda: self.change_gender(self.ui.radioButton_2,"women")
        )

        self.ui.uielem_startSearch.clicked.connect(self.start_search)

    # Функция смены цвета (комбо бокса)
    def change_color(self):
        color_names = [
            "Red",
            "Red-Orange",
            "Pink-Red",
            "Pink",
            "Magenta-Pink",
            "Magenta",
            "Blue-Magenta",
            "Blue",
            "Cyan-Blue",
            "Cyan",
            "Green-Cyan",
            "Green",
            "Yellow-Green",
            "Yellow",
            "Orange-Yellow",
            "Orange-Brown"
        ]

        self.params.update({
            'hair_color': color_names[self.ui.ui_hairColorComboBox.currentIndex()]
        })

    # Функция смены типа волос
    def change_hair_type(self):
        hair_type_names = ["normal", "greasy", "dry", "mixed"]
        self.params.update({
            'hair_type': hair_type_names[self.ui.ui_hairTypeComboBox.currentIndex()]
        })

    # Функция смены длины волос
    def change_hair_length(self):
        hair_length_names = ["short", "medium", "long"]
        self.params.update({
            'hair_length': hair_length_names[self.ui.ui_hairLengthComboBox.currentIndex()]
        })

    # Функция смены пола
    def change_gender(self, radio_button, gender):
        if (radio_button.text() == "Мужчина" or radio_button.text() == "Женщина" )and radio_button.isChecked() is True:
            self.params.update({
                'gender': gender
            })
            self.ui.uielem_startSearch.setEnabled(True)

    # Функция запуска поиска
    def start_search(self):
        templates = self.server_class.get_templates(self.params).get("message").get("paths_to_image")
        print(templates)
        GalleryWin(self, templates=templates).show()


'''
    Класс отображения галереи фотографий после поиска
'''


class GalleryWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, templates=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_ListViewWindow()
        self.ui.setupUi(self)

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())
        # Настрока размеров
        self.ui.listWidget.setGridSize(QtCore.QSize(300,300))
        self.ui.listWidget.setUniformItemSizes(True)
        # Отключение Drag And Drop
        self.ui.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.setAcceptDrops(False)

        #self.ui.listWidget.itemClicked.connect(self.item_click)

        for url in templates:
            url = '../server/' + url
            icon = QtGui.QIcon(url)
            pixmap = icon.pixmap(150, 150)
            icon = QtGui.QIcon(pixmap)
            item = QtWidgets.QListWidgetItem(url)
            item.setIcon(icon)
            self.ui.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    # def item_click(self, item):
    #     print(str(item.text()))


'''
    Основной класс для работы с интерфейсом камеры
'''


class WebCamWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, video_class=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_WebCamWindow()
        self.ui.setupUi(self)

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())

        self.ui.ui_makePhoto.clicked.connect(self.crop_face)

        self.video = video_class(cv2.VideoCapture(0))

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()

    def play(self):
        try:
            self.video.capture_next_frame()
            pixmap = self.video.convert_frame().get("img")
            self.ui.videoFrame.setPixmap(
                pixmap
            )
            self.ui.videoFrame.setScaledContents(True)
        except TypeError:
            print("No frame")

    def crop_face(self):
        self.video.get_face(self.video.convert_frame().get("face"))
        self.close()


'''
    Основной класс для манипуляций со всеми окнами приложения
'''


class ShowWindow:
    @staticmethod
    def show_error_win(error_message):
        app = QtWidgets.QApplication(sys.argv)
        my_app = ErrorWin(error_message=error_message)
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_vote_win(server_class):
        app = QtWidgets.QApplication(sys.argv)
        my_app = VoteWin(server_class=server_class)
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_main_win(server_class):
        app = QtWidgets.QApplication(sys.argv)
        my_app = MainWin(server_class=server_class)
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_gallery_win(parent=None):
        app = QtWidgets.QApplication(sys.argv)
        my_app = GalleryWin()
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_web_cam_win(video_class):
        app = QtWidgets.QApplication(sys.argv)
        my_app = WebCamWin(video_class=video_class)
        my_app.show()
        sys.exit(app.exec_())