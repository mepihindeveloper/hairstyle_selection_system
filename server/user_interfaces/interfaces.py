import sys
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from server.user_interfaces._py.ui_archives import Ui_Archives
from server.user_interfaces._py.ui_server_main import Ui_ServerMain


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
            result = self.backup_class.restore()
            QtWidgets.QMessageBox.information(self, "Информация о действии", result.get("message"))


class ServerWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, server=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_ServerMain()
        self.ui.setupUi(self)
        self.server = server()

        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())
        self.ui.ui_StartServer.clicked.connect(self.server_start)
        self.ui.ui_StopServer.clicked.connect(self.server_stop)
        self.ui.ui_ArchivesOpen.clicked.connect(self.start_archives_utility)

    def server_start(self):
        result = self.server.start()
        QtWidgets.QMessageBox.information(self, "Информация о сервере", result.get("message"))

    def server_stop(self):
        result = self.server.stop()
        QtWidgets.QMessageBox.information(self, "Информация о сервере", result.get("message"))

    def start_archives_utility(self):
        self.hide()
        os.system("python backup.py")
        self.show()


class ShowWindow:
    @staticmethod
    def show_archive_win(backup_class=None):
        app = QtWidgets.QApplication(sys.argv)
        my_app = ArchivesWin(backup_class=backup_class)
        my_app.show()
        sys.exit(app.exec_())

    @staticmethod
    def show_server_main_win(server=None):
        app = QtWidgets.QApplication(sys.argv)
        my_app = ServerWin(server=server)
        my_app.show()
        sys.exit(app.exec_())
