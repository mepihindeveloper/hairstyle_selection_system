# coding: utf8
import socketserver
import sqlite3
import datetime
import pickle
import threading

from user_interfaces.interfaces import ShowWindow


class Handler(socketserver.BaseRequestHandler):
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

    def __add_rating_to_db(self, client_id, rating, service):
        # Устанавливаем соединение
        self.__connection()
        date_now = datetime.datetime.now()

        self.cursor.execute(
            "SELECT * FROM local_statistics WHERE date = '{}' AND client_id='{}'".format(
                date_now.strftime("%Y-%m-%d"),
                client_id
            )
        )
        row = self.cursor.fetchone()
        if row is None:
            self.cursor.execute(
                "INSERT INTO local_statistics (client_id, date, " + rating + " ,service) VALUES ('{}', '{}', '1' ,'{}')".format(
                    client_id,
                    date_now.strftime("%Y-%m-%d"),
                    service
            ))

        else:
            self.cursor.execute(
                "UPDATE local_statistics SET " + rating + " = " + rating + " + 1 WHERE date = '{}' AND client_id='{}'".format(
                    date_now.strftime("%Y-%m-%d"),
                    client_id
                )
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

    def get_templates(self, hair_type, hair_length, hair_color, gender):
        self.__connection()
        self.cursor.execute(
            "SELECT path_to_image FROM local_hairstyle_images "
            "WHERE hair_type = '{}' AND hair_length = '{}' AND hair_color = '{}' AND gender = '{}'".format(
                hair_type,
                hair_length,
                hair_color,
                gender
            )
        )
        row = self.cursor.fetchone()
        templates = []
        while row is not None:
            templates.append(row[0])
            row = self.cursor.fetchone()

        return templates

    def handle(self):
        while True:
            self.data = pickle.loads(self.request.recv(4096))

            print('Клиент {} отпрвил сообщение: {}'.format(
                self.client_address, self.data)
            )

            if self.data:
                if self.data.get("command") == 'CHECK_LICENSE':
                    result = self.get_license_status(
                        self.data.get("message").get("license_key")
                    )
                    if result is True:
                        self.request.send(pickle.dumps({
                            'command': 'VERIFIED'
                        }))
                    else:
                        self.request.send(pickle.dumps({
                            'command': 'NOT_VERIFIED'
                        }))
                elif self.data.get("command") == 'GOODBYE':
                    break
                elif self.data.get("command") == 'RATING':
                    self.__add_rating_to_db(
                        self.data.get("message").get("client_id"),
                        self.data.get("message").get("rating"),
                        self.data.get("message").get("service")
                    )
                    self.request.send(pickle.dumps({
                        'command': 'RATING-ADDED'
                    }))
                elif self.data.get("command") == 'GET_TEMPLATES':
                    result = self.get_templates(
                        self.data.get("message").get("hair_type"),
                        self.data.get("message").get("hair_length"),
                        self.data.get("message").get("hair_color"),
                        self.data.get("message").get("gender")
                    )
                    self.request.send(pickle.dumps({
                        'command': 'FINDED_TEMPLATES',
                        'message': {
                            'paths_to_image': result
                        }
                    }))
            else:
                break
        print('Разрыв соединения с ', self.client_address[0])
        self.__disconnect()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Server:
    server = None

    def start(self):
        self.server = ThreadedTCPServer(('localhost', 10000), Handler)

        ip, port = self.server.server_address
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Сервер работает в потоке:", server_thread.name)
        return {"status": True, "message": "Сервер работает в потоке: {}".format(server_thread.name)}

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        print('Сервер остановлен')
        return {"status": False, "message": "Сервер остановлен"}


if __name__ == '__main__':
    ShowWindow.show_server_main_win(server=Server)
