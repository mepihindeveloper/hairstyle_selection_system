import sys
import numpy as np
import cv2
import imutils

from PyQt5 import QtWidgets, QtGui, QtCore
from ._py.ui_design import Ui_MainWindow
from ._py.ui_vote_dialog import Ui_VoteDialog
from ._py.ui_error_dialog import Ui_ErrorDialog
from ._py.ui_listviewimages import Ui_ListViewWindow
from ._py.ui_web_cam import Ui_WebCamWindow


'''
    Вспомогательный класс для работы с камерой
    Включает в себя наложения и прочие функции для работы именно с видеопотоком и элементами
'''


class ImageProcessing:
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = np.array([])
        self.face = None
        self.overlay_image = cv2.imread("image_2.png", -1)

    def capture_next_frame(self):
        """
        capture frame and reverse RBG BGR and return opencv image
        """
        (ret, readFrame) = self.capture.read()
        if ret is True:
            readFrame = cv2.flip(readFrame, 1)
            self.face = self.blend_transparent(bg_image=readFrame, overlay_t_img=self.overlay_image)
            self.currentFrame = cv2.cvtColor(self.face, cv2.COLOR_BGR2RGB)

    def convert_frame(self):
        """     converts frame to format suitable for QtGui            """
        try:
            height, width = self.currentFrame.shape[:2]
            img = QtGui.QImage(self.currentFrame,
                               width,
                               height,
                               QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return {'img': img, 'face': self.face}
        except:
            return None

    def blend_transparent(self, bg_image, overlay_t_img):
        # Разделите маску прозрачности из информации о цвете
        overlay_img = overlay_t_img[:, :, :3]  # Возьмите плоскости BRG
        overlay_mask = overlay_t_img[:, :, 3:]  # И alpha плоскость

        # Снова вычислите обратную маску
        background_mask = 255 - overlay_mask

        # Поверните маски в три канала, чтобы мы могли использовать их в качестве весов
        overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

        # Создайте замаскированное изображение лица и замаскируйте наложение
        # Мы преобразуем изображения в плавающие точки в диапазоне 0.0 - 1.0
        face_part = (bg_image * (1 / 255.0)) * (background_mask * (1 / 255.0))
        overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

        # И, наконец, просто добавьте их вместе и измените размер до 8-битного целого изображения
        return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

    def get_face(self, face):
        # Преобразуем в серые тона
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        # Делаем небольшое размытие, чтобы исключи микроразрывы контура
        gray = cv2.medianBlur(gray, 3)

        (ret, thresh) = cv2.threshold(gray, 1, 255, 0)
        (im2, contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Порог изображения, затем выполните серию эрозий + растяжения, чтобы удалить любые небольшие области шума
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Найти контуры в пороговом изображении, а затем захватить самую большую
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        c = max(cnts, key=cv2.contourArea)

        (x, y, w, h) = cv2.boundingRect(c)
        face = face[y: y + h, x: x + w]
        cv2.imwrite("temp.png", face)

        self.make_transparent("temp.png")

    def release(self):
        self.capture.release()

    def make_transparent(self, image_path):
        image = cv2.imread(image_path, 1)
        tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(image)

        rgba = [b, g, r, alpha]
        image = cv2.merge(rgba, 4)

        cv2.imwrite("temp.png", image)

    def overlay_face_to_hair(self, hair_image_path):
        '''

        :param hair_image_path: Путь к файлу с прической
        :return: готовая фотография
        '''
        face_img = cv2.imread("client/temp.png", -1)
        hair_image = cv2.imread(hair_image_path, -1)

        x_offset = int((hair_image.shape[1] / 2) - (face_img.shape[1] / 2))
        y_offset = int((hair_image.shape[0] / 2) - (face_img.shape[0] / 2))

        y1, y2 = y_offset, y_offset + face_img.shape[0]
        x1, x2 = x_offset, x_offset + face_img.shape[1]

        alpha_s = face_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            hair_image[y1:y2, x1:x2, c] = (alpha_s * face_img[:, :, c] + alpha_l * hair_image[y1:y2, x1:x2, c])


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
        self.is_photo_done = False

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
        if self.is_photo_done is not True:
            # Сначала фотографируем клиента
            WebCamWin(self).show()
            self.ui.uielem_startSearch.setText("Поиск")
            self.is_photo_done = True
        else:
            # Производим поиск
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
    def __init__(self, parent=None, ):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_WebCamWindow()
        self.ui.setupUi(self)
        # Отключаем возможность изменения разамера окна
        self.setFixedSize(self.size())

        self.ui.ui_makePhoto.clicked.connect(self.crop_face)

        self.video = ImageProcessing(cv2.VideoCapture(0))

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
        self.video.release()
        self.close()


'''
    Основной класс для манипуляций со всеми окнами приложения
'''


class ShowWindow():
    @staticmethod
    def show_main_win(server_class):
        app = QtWidgets.QApplication(sys.argv)
        my_app = MainWin(server_class=server_class)
        my_app.show()
        sys.exit(app.exec_())