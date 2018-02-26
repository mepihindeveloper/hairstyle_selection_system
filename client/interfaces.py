import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from .user_interfaces._py.ui_design import *
from .user_interfaces._py.ui_vote_dialog import *
from .user_interfaces._py.ui_error_dialog import *


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
