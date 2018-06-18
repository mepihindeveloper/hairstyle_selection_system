import sys
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from ._py.ui_archives import Ui_Archives
from ._py.ui_server_main import Ui_ServerMain
from ._py.ui_initialization import Ui_Initialization


class ArchivesWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, backup_class=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Archives()
        self.ui.setupUi(self)
        self.backup_class = backup_class()
        self.item = None

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())

        # Отключение Drag And Drop
        self.ui.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.setAcceptDrops(False)

        self.ui.listWidget.itemClicked.connect(self.item_click)
        self.ui.ui_MakeCopy.clicked.connect(self.make_archive)
        self.ui.ui_ResetCopy.clicked.connect(self.restore_archive)

        self.update_archives()

    def update_archives(self):
        self.ui.listWidget.clear()
        archives = [
            os.path.join("../backups/", name)
            for dir_path, dirs, files in
            os.walk("../backups/")
            for name in files
            if name.endswith(".zip")
        ]

        for url in archives:
            item = QtWidgets.QListWidgetItem(url)
            self.ui.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def make_archive(self):
        result = self.backup_class.make_zip()
        QtWidgets.QMessageBox.information(self, "Информация о действии", result.get("message"))
        self.update_archives()

    def item_click(self, item):
        self.item = str(item.text())

    def restore_archive(self):
        if self.item is not None:
            result = self.backup_class.restore(archive=self.item)
            QtWidgets.QMessageBox.information(self, "Информация о действии", result.get("message"))


class ServerWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, server=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_ServerMain()
        self.ui.setupUi(self)
        self.server = server()

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())
        self.ui.ui_StopServer.setEnabled(False)
        self.ui.ui_StartServer.clicked.connect(self.server_start)
        self.ui.ui_StopServer.clicked.connect(self.server_stop)
        self.ui.ui_ArchivesOpen.clicked.connect(self.start_archives_utility)
        self.ui.ui_TemplatesUpdate.clicked.connect(self.start_initialization)

    def server_start(self):
        result = self.server.start()
        QtWidgets.QMessageBox.information(self, "Информация о сервере", result.get("message"))
        self.ui.ui_StartServer.setEnabled(False)
        self.ui.ui_StopServer.setEnabled(True)

    def server_stop(self):
        result = self.server.stop()
        QtWidgets.QMessageBox.information(self, "Информация о сервере", result.get("message"))
        self.ui.ui_StartServer.setEnabled(True)
        self.ui.ui_StopServer.setEnabled(False)

    def start_archives_utility(self):
        self.hide()
        os.system("python backup.py")
        self.show()

    def start_initialization(self):
        self.hide()
        os.system("python initialization.py")
        self.show()


class InitializationWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, initialisation_class=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Initialization()
        self.ui.setupUi(self)
        self.initialisation_class = initialisation_class
        self.hair_type_name = 'normal'
        self.i = 0

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())

        # подключение функций
        self.ui.ui_HairType.currentIndexChanged.connect(self.change_hair_type)
        self.ui.ui_SaveButton.clicked.connect(self.save_photo)

        self.photos = self.initialisation_class.initialization_files()
        self.change_photo(self.photos[self.i])

    def change_photo(self, photo_url):
        pixmap = QtGui.QPixmap(photo_url)
        self.ui.ui_Image.setPixmap(pixmap)

    # Функция смены типа волос
    def change_hair_type(self):
        hair_type_names = ["normal", "greasy", "dry", "mixed"]
        self.hair_type_name = hair_type_names[self.ui.ui_HairType.currentIndex()]

    def save_photo(self):
        self.initialisation_class.generate_hairstyle_structure(
            hair_type=self.hair_type_name,
            template=self.photos[self.i]
        )
        if (self.i == (len(self.photos) -1)):
            self.initialisation_class.save()
            self.close()
        else:
            self.i += 1
            self.change_photo(self.photos[self.i])

class ShowWindow:
    @staticmethod
    def show_archive_win(backup_class=None):
        app = QtWidgets.QApplication(sys.argv)
        my_app = ArchivesWin(backup_class=backup_class)
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_initialization_win(initialisation_class=None):
        app = QtWidgets.QApplication(sys.argv)
        my_app = InitializationWin(initialisation_class=initialisation_class)
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_server_main_win(server=None):
        app = QtWidgets.QApplication(sys.argv)
        my_app = ServerWin(server=server)
        my_app.show()
        sys.exit(app.exec_())
