import socketserver
import sqlite3
import datetime

_HOST = 'localhost'
_PORT = 9999
_CLIENTS = []

class __Handler(socketserver.BaseRequestHandler):
    conn = None # Коннектор
    c = None # Курсор

    def __connection(self):
        # Подключение к БД
        self.conn = sqlite3.connect('main_db.db')
        self.c = self.conn.cursor()

    def __disconnect(self):
        self.c.close()
        self.conn.close()

    def _check_license(self, license_key):
        self.__connection()
        self.c.execute('SELECT * FROM clients')
        row = self.c.fetchone()

        while row is not None:
            if row[1] == license_key:
                reg_date = datetime.datetime.strptime("2016-12-06", "%Y-%m-%d").date()
                if reg_date.year > datetime.datetime.today().year + 1 and reg_date.month == datetime.datetime.today().month \
                        and reg_date.day == datetime.datetime.today().day:
                    # закрываем соединение с базой
                    self.__disconnect()
                    return False
                else:
                    # закрываем соединение с базой
                    self.__disconnect()
                    return True
            row = self.c.fetchone()

    def __add_rating_to_db(self, rating, license_key):
        # Устанавливаем соединение
        self.__connection()

        self.c.execute("SELECT * FROM clients WHERE license_key = '%s'" % license_key)
        row = self.c.fetchone()
        if row is not None:
            if rating == "y":
                new_rating = row[3] + 1
                self.c.execute("UPDATE clients SET yes = '%i' WHERE license_key = '%s' " % (new_rating, license_key))
            else:
                new_rating = row[4] + 1
                self.c.execute("UPDATE clients SET no = '%i' WHERE license_key = '%s' " % (new_rating, license_key))

            self.conn.commit()
        # Отключение
        self.__disconnect()

    def handle(self):
        self.data = self.request.recv(1024).decode()
        _CLIENTS.append(self.client_address)
        print('Client {} reports: {}'.format(self.client_address[0], self.data))

        if self.data == 'CONNECTED':
            self.request.sendall(bytes('OK', 'utf-8'))
            while True:
                self.data = self.request.recv(1024).decode()
                resp = self.data.split(';')
                print(resp)

                if resp[0] == 'TRY':
                    self.__add_rating_to_db(resp[1], resp[2])
                    self.request.sendall(bytes('WRITED', 'utf-8'))
                elif resp[0] == 'CHECK_LICENSE':
                    result = self._check_license(resp[1])
                    if result == True:
                        self.request.sendall(bytes('VERIFIED', 'utf-8'))
                    else:
                        self.request.sendall(bytes('NOT_VERIFIED', 'utf-8'))
                elif resp[0] == 'GOODBYE':
                    break
                else:
                    print('Unknown request from the user.')
                    break
        else:
            print('Unknown request from a client.')


server = socketserver.TCPServer((_HOST, _PORT), __Handler)
print('The server is running')
server.serve_forever()