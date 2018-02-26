import socketserver
import sqlite3
import datetime


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

    def __add_rating_to_db(self, rating, service):
        # Устанавливаем соединение
        self.__connection()
        date_now = datetime.datetime.now()

        self.cursor.execute(
            "SELECT * FROM statistics WHERE date = '{}'".format(
                date_now.strftime("%Y-%m-%d"))
        )
        row = self.cursor.fetchone()
        if row is None:
            self.cursor.execute(
                "INSERT INTO statistics (date, service) VALUES ('{}', '{}')".format(
                    date_now.strftime("%Y-%m-%d"),
                    service
            ))

        else:
            self.cursor.execute(
                "UPDATE statistics SET " + rating + " = " + rating + " + 1 WHERE date = '{}'".format(
                    date_now.strftime("%Y-%m-%d"))
            )
        self.connection.commit()

    def get_license_status(self, license_key):
        self.__connection()
        self.cursor.execute('SELECT * FROM clients')
        row = self.cursor.fetchone()

        while row is not None:
            if row[1] == license_key:
                # Получаем дату регистрации продукта
                reg_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()

                # Получаем текущую дату в формате "%Y-%m-%d"
                year = datetime.datetime.now().year
                month = datetime.datetime.now().month
                day = datetime.datetime.now().day
                current_date = datetime.datetime.strptime("{}-{}-{}".format(year, month, day), "%Y-%m-%d").date()

                # Считаем разницу в днях
                different_of_dates = str(current_date - reg_date).split()[0]
                different_of_dates = int(different_of_dates)

                if 0 <= different_of_dates <= 365:
                    return True
                else:
                    return False

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
                elif data_parts[0] == 'RATING':
                    self.__add_rating_to_db(data_parts[1], data_parts[2])
                    self.request.send(bytes('RATING-ADDED', 'utf-8'))
            else:
                break
        print('Разрыв соединения с ', self.client_address[0])
        self.__disconnect()


server = socketserver.TCPServer(('localhost', 10000), __Handler)
print('Сервер запущен')
server.serve_forever()