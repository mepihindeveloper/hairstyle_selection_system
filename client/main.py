import socket
import pickle
import configparser

from client.user_interfaces.interfaces import *

#license_key = None
client_settings = {}

'''
    Класс для работы с сервером
    Влючает в себя функции для общения с TCP сервером
'''


class ServerFunctions:
    def __init__(self):
        self.sock = None

    # Функция установки соединения с сервером
    def __connection(self):
        # Теперь устанавливаем соединения с сервером. Если успешно, то продолжаем, иначе - выход из программы
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = self.sock.connect_ex(('localhost', 10000))
        if result:
            return {"status": False, "message": "Подключение к серверу отсутствует.\nСервер временно выключен"}
        else:
            return {"status": True}

    # Функция закрытия соединения
    def __disconnect(self):
        self.sock.sendall(pickle.dumps({
            'command': 'GOODBYE'
        }))
        self.sock.close()

    # Функция отправки даных на сервер
    def __send_data(self, data={'command': None, 'message': None}):
        self.sock.sendall(pickle.dumps(data))
        return pickle.loads(self.sock.recv(4096))

    #  Функция проверка статуса лицензии
    '''def get_license_status(self):
        global license_key

        # Проверка файла лицензии на существование
        # Если есть, то запишем в переменную ее содержимое
        # Иначе вернем ошибку
        try: file = open('license', 'r')
        except IOError as error: return {"status": False, "message": "Файл лицензии отсутствует!\n{}".format(error)}
        else:
            with file:
                license_key = file.readline()
                file.close()

        result = self.__connection()
        # Выполняем подключение к базе данных
        if result.get("status") is not True:
            return result

        # Так как установлено соединение с сервером, то необходимо проверить лицензию по ключу
        # Если срок не истек, то разрешаем пользоваться программой, иначе выходим из программы
        received = self.__send_data(data={
            'command': 'CHECK_LICENSE',
            'message': {
                'license_key': license_key
            }
        })
        self.__disconnect()
        if received.get("command") == "VERIFIED":
            return {"status": True, "message": "Лицензия подтверждена"}
        else:
            return {"status": False, "message": "У вас нет лицензии!"}
    '''

    # Функция оценки результатов
    def set_rating(self, rating='positive'):
        global client_settings

        result = self.__connection()
        # Выполняем подключение к базе данных
        if result.get("status") is not True:
            return result

        received = self.__send_data(data={
            'command': 'RATING',
            'message': {
                'client_id': client_settings.get('id'),
                'rating': rating,
                'service': 'haircut'
            }
        })
        self.__disconnect()
        if received.get("command") == 'RATING-ADDED':
            return {"status": True, "message": "Спасибо за оценку!\nГолос учтен"}
        else:
            return {"status": False, "message": "Произошла ошибки при оценке!"}

    # Функция для получения списка фотографий выборки
    def get_templates(self, params={}):
        result = self.__connection()
        if result.get("status") is not True:
            return result

        received = self.__send_data(data={
            'command': 'GET_TEMPLATES',
            'message': params
        })
        self.__disconnect()

        return received


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
    Работа с INI файлами конфигурации
'''


class Ini:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.file_name = 'settings.ini'

    def read_file(self):
        try:
            file = open(self.file_name, 'r')
        except IOError as error:
            return {"status": False, "message": "Файл настроек отсутствует!\n{}".format(error)}
        else:
            with file:
                self.config.read(self.file_name)
                file.close()
                return {"status": True}

    def get_value(self, section, key):
        file_exist = self.read_file()
        if file_exist.get("status") is True:
            return {"status": True, "value": self.config[section][key]}
        else:
            return file_exist


if __name__ == "__main__":
    app = my_app = None
    ini = Ini()
    client_id = ini.get_value("client_settings", 'id')
    place = ini.get_value("client_settings", 'place')

    if client_id.get("status") is True and place.get("status") is True:
        client_settings.update({
            'id': client_id.get("value"),
            'place': place.get("value")
        })

    server_functions = ServerFunctions()

    #server_functions = ServerFunctions()
    #result = server_functions.get_license_status()

    # if result.get("status") is not True:
    #     ShowWindow.show_error_win(error_message=result.get("message"))
    # else:
    #     #ShowWindow.show_vote_win(server_class=server_class)
    #     ShowWindow.show_main_win(server_class=server_functions)

    #ShowWindow.show_gallery_win()
    #print(server_class.get_templates(params=['mixed', 'long', 'Orange-Brown', 'women']))
    #ShowWindow.show_web_cam_win(video_class=ImageProcessing)
