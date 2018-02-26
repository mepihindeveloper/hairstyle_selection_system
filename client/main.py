import socket
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

    # Функция закрытия соединения
    def __disconnect(self):
        self.sock.sendall(bytes("GOODBYE", 'utf-8'))
        self.sock.close()

    # Функция отправки даных на сервер
    def __send_data(self, command, data=[]):
        '''

        :param command: Команда для сервера, находящаяся перед разделителем ";"
        :param data: Данные (сообщение) для сервера
        :return: Ответ от сервера
        '''

        # В случае, если данных для команды много, то формируем запрос иначе
        if len(data) > 1:
            data = '=>'.join(data)
        else:
            data = data[0]

        self.sock.sendall(bytes("{}=>{}".format(command, data), 'utf-8'))
        return self.sock.recv(1024).decode()

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

        # Выполняем подключение к базе данных
        if self.__connection():
            return {"status": False, "message": "Подключение к серверу отсутствует.\nСервер временно выключен"}

        # Так как установлено соединение с сервером, то необходимо проверить лицензию по ключу
        # Если срок не истек, то разрешаем пользоваться программой, иначе выходим из программы
        received = self.__send_data('CHECK_LICENSE', [license_key])

        if received == "VERIFIED":
            self.__disconnect()
            return {"status": True, "message": "Лицензия подтверждена"}
        else:
            return {"status": False, "message": "У вас нет лицензии!"}

    # Функция оценки результатов
    def set_rating(self, rating='positive'):
        global license_key
        # Выполняем подключение к базе данных
        if self.__connection():
            return {"status": False, "message": "Подключение к серверу отсутствует.\nСервер временно выключен"}

        received = self.__send_data('RATING', [rating, 'haircut'])
        if received == 'RATING-ADDED':
            return {"status": True, "message": "Спасибо за оценку!\nГолос учтен"}
        else:
            return {"status": False, "message": "Произошла ошибки при оценке!"}


if __name__ == "__main__":
    app = my_app = None
    server_class = ServerFunction()
    result = server_class.get_license_status()

    if result.get("status") is not True:
        ShowWindow.show_error_win(error_message=result.get("message"))
    else:
        ShowWindow.show_vote_win(server_class=server_class)