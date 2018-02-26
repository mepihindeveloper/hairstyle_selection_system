import socket
import pickle
from client.interfaces import ShowWindow

license_key = None

'''
    Класс для работы с сервером
    Влючает в себя функции для общения с TCP сервером
'''


class ServerFunction:
    sock = None

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
    def get_license_status(self):
        global license_key

        '''
            Проверка файла лицензии на существование
            Если есть, то запишем в переменную ее содержимое
            Иначе вернем ошибку
        '''
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

    # Функция оценки результатов
    def set_rating(self, rating='positive'):
        result = self.__connection()
        # Выполняем подключение к базе данных
        if result.get("status") is not True:
            return result

        received = self.__send_data(data={
            'command': 'RATING',
            'message': {
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


if __name__ == "__main__":
    app = my_app = None
    server_class = ServerFunction()
    result = server_class.get_license_status()

    if result.get("status") is not True:
        ShowWindow.show_error_win(error_message=result.get("message"))
    else:
        #ShowWindow.show_vote_win(server_class=server_class)
        ShowWindow.show_main_win(server_class=server_class)

    #print(server_class.get_templates(params=['mixed', 'long', 'Orange-Brown', 'women']))

