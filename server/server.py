import socketserver
import sqlite3
import datetime

_HOST = 'localhost'
_PORT = 10000


class __Handler(socketserver.BaseRequestHandler):
    params = {
        'database': './database/main_db.db'
    }
    connection = None  # Коннектор
    cursor = None  # Курсор

    def __connection(self):
        # Подключение к БД
        self.connection = sqlite3.connect(self.params.get('database'))
        self.cursor = self.connection.cursor()

    def __disconnect(self):
        self.cursor.close()
        self.connection.close()

    def __add_rating_to_db(self, rating, license_key):
        # Устанавливаем соединение
        self.__connection()

        date_now = datetime.datetime.now()
        self.cursor.execute(
            "UPDATE statistics SET " + rating + " = " + rating + " + 1 WHERE date = '{}'-".format(
                date_now.strftime("%Y-%m-%d"))
        )
        self.connection.commit()

        # Отключение
        self.__disconnect()

    def get_license_status(self, license_key):
        self.__connection()
        self.cursor.execute('SELECT * FROM clients')
        row = self.cursor.fetchone()

        while row is not None:
            if row[1] == license_key:
                reg_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
                if reg_date.year > datetime.datetime.today().year + 1 and reg_date.month == datetime.datetime.today().month \
                        and reg_date.day == datetime.datetime.today().day:
                    return False
                else:
                    return True
            row = self.cursor.fetchone()

    def handle(self):
        while True:
            self.data = self.request.recv(1024).decode('utf-8')
            print('Клиент {} отпрвил сообщение: {}'.format(self.client_address, self.data))

            if self.data:
                data_parts = self.data.split('=>')
                if data_parts[0] == 'CHECK_LICENSE':
                    result = self.get_license_status(data_parts[1])
                    if result is True:
                        self.request.send(bytes('VERIFIED', 'utf-8'))
                    else:
                        self.request.send(bytes('NOT_VERIFIED', 'utf-8'))
                elif data_parts[0] == 'GOODBYE':
                    break
            else:
                break
        print('Разрыв соединения с ', self.client_address[0])
        self.__disconnect()
        # if self.data == 'CONNECTED':
        #     self.request.sendall(bytes('OK', 'utf-8'))
        #     while True:
        #         self.data = self.request.recv(1024).decode()
        #         resp = self.data.split(';')
        #         print(resp)
        #
        #         if resp[0] == 'TRY':
        #             self.__add_rating_to_db(resp[1], resp[2])
        #             self.request.sendall(bytes('WRITED', 'utf-8'))
        #         elif resp[0] == 'CHECK_LICENSE':
        #             result = self.get_license_status(resp[1])
        #             if result is True:
        #                 self.request.sendall(bytes('VERIFIED', 'utf-8'))
        #             else:
        #                 self.request.sendall(bytes('NOT_VERIFIED', 'utf-8'))
        #         elif resp[0] == 'GOODBYE':
        #             break
        #         else:
        #             print('Unknown request from the user.')
        #             break
        # else:
        #     print('Unknown request from a client.')


server = socketserver.TCPServer((_HOST, _PORT), __Handler)
print('Сервер запущен')
server.serve_forever()