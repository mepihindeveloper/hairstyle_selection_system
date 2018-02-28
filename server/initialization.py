# coding: utf8
import sqlite3
import os
import random
import cv2
import numpy as np

hairstyle_templates = {
    'men': {
        'templates': {}
    },
    'women': {
        'templates': {}
    }
}
hair_length_associate = {
    'short': {
        'min': 10,
        'max': 459
    },
    'medium': {
        'min': 460,
        'max': 549
    },
    'long': {
        'min': 550,
        'max': 999
    }
}


class Initialization:
    # Параметры системы инициализации
    params = {
        'path_to_hairstyles': 'hairstyle_images',
        'path_to_men_hairstyles': "/men",
        'path_to_women_hairstyles': "/women",
        'hair_types': ["normal", "greasy", "dry", "mixed"],
        'database': 'database/main_db.db',
        'debug': False
    }

    connection = cursor = None

    def __init__(self, params={}):
        for param in params:
            if param is not None:
                self.params.update({param: params.get(param)})

    # Функция уставновки соединения с БД
    def __init_connection(self):
        self.connection = sqlite3.connect(self.params.get('database'))
        self.cursor = self.connection.cursor()

    # Функция разрыва соединения
    def __exit_connection(self):
        self.cursor.close()
        self.connection.close()

    # Основная функция инициализации
    def initialization(self):
        # Установка соединения и назначение курсора
        self.__init_connection()

        # Очищаем базу данных от возмжных записей (предусматривается, что их не должно быть)
        self.cursor.execute("DELETE FROM hairstyle_images")

        # Получаем все картинки из выбранной папки
        print("Сканирование женских шаблонов...")
        dir_and_subdir_templates = [
            os.path.join(self.params.get('path_to_hairstyles') + self.params.get('path_to_women_hairstyles'), name)
            for dir_path, dirs, files in os.walk(self.params.get('path_to_hairstyles') + self.params.get('path_to_women_hairstyles'))
            for name in files
            if name.endswith((".jpg", ".png", ".jpeg"))
        ]

        if self.params.get('debug') is True:
            print(dir_and_subdir_templates)

        # Генерируем структуры для шаблонов причесок
        self.__generate_hairstyle_structure(dir_and_subdir_templates)

        # Добавляем новые строки в базу данных
        self.__insert_into_db(self.connection, self.cursor)

        # Разрыв соединения с БД
        self.__exit_connection()

    # Функция добавления новых записей в базу данных
    def __insert_into_db(self, connection, cursor):
        '''

        :param connection: Активное соединение с базой данных
        :param cursor: Курсор управления запросами и БД
        :return:
        '''
        global hairstyle_templates
        for item in hairstyle_templates.get('women').get('templates'):
            cursor.execute("INSERT INTO hairstyle_images "
                           "(path_to_image, hair_type, hair_length, hair_color, gender) "
                           "VALUES ('%s', '%s', '%s', '%s','%s')" % (
                               hairstyle_templates.get('women').get('templates').get(item)['path'],
                               hairstyle_templates.get('women').get('templates').get(item)['type'],
                               hairstyle_templates.get('women').get('templates').get(item)['length'],
                               hairstyle_templates.get('women').get('templates').get(item)['color'],
                               'women'
                           )
                           )
            connection.commit()

    # Функция генерации структуры для шаблонов причесок
    def __generate_hairstyle_structure(self, dir_and_subdir_templates):
        global hairstyle_templates
        i = 0
        '''
            Цикл прхода по всем шаблонам из найденных в dir_and_subdir_templates
            Идет считываение типа волос путем ввода вручную
            Процесс определения длины волос напрямую зависит от высоты фото (условие задачи и ее рациональность)
            Процесс получения лидирующего цвета по HSV (для точности выделяется 3 цвета)
            Формируется новый словарь по шаблону
            Добавляется в общую структуру
        '''
        for template in dir_and_subdir_templates:
            # hair_type = input("Введите тип волос (normal, greasy, dry, mixed): ")
            # while hair_type not in self.params.get('hair_types'):
            #    print("Ошибка: вы можете ввести только значения: normal, greasy, dry, mixed")
            #    hair_type = input("Введите тип волос (normal, greasy, dry, mixed): ")

            hair_type = random.choice(self.params.get('hair_types'))
            length = self.__detect_hair_length(template)
            color = self.__detect_primary_colors(template)[0]
            new_template = {
                'item_{}'.format(i): {
                    'path': template,
                    'type': hair_type,
                    'length': length,
                    'color': color
                }
            }

            hairstyle_templates.get('women').get('templates').update(new_template)
            i += 1

    # Функция определения длины волос
    def __detect_hair_length(self, single_template):
        '''

        :param single_template: Путь к изображнию шаблона для анализа
        :return: Длина волос
        '''
        global hair_length_associate
        single_template = cv2.imread(single_template)
        length = None

        # Задается математическое выражение, что если длина >= минимальной и длина <= максимальной
        for item in hair_length_associate:
            if hair_length_associate.get(item)['min'] <= int(single_template.shape[0]) <= \
                    hair_length_associate.get(item)['max']:
                length = item
        return length

    # Функция опредеоения лидирующих цветов
    def __detect_primary_colors(self, single_template):
        '''

        :param single_template: Путь к изображнию шаблона для анализа
        :return: Массив трех лидируюших цветов
        '''
        single_photo = cv2.imread(single_template)
        hue_color_name = [
            [355, 360, "Red"],
            [346, 355, "Pink-Red"],
            [331, 345, "Pink"],
            [321, 330, "Magenta-Pink"],
            [281, 320, "Magenta"],
            [241, 280, "Blue-Magenta"],
            [221, 240, "Blue"],
            [201, 220, "Cyan-Blue"],
            [170, 200, "Cyan"],
            [141, 169, "Green-Cyan"],
            [81, 140, "Green"],
            [61, 80, "Yellow-Green"],
            [51, 60, "Yellow"],
            [41, 50, "Orange-Yellow"],
            [21, 40, "Orange-Brown"],
            [11, 20, "Red-Orange"],
            [1, 10, "Red"]
        ]

        '''
            Конвертация в HSV для работы
            Нарезка HSV на составляющие hue, saturation, value
            Постороение гистограммы по модели HSV
        '''
        hsv = cv2.cvtColor(single_photo, cv2.COLOR_BGR2HSV)
        hue, s, v = cv2.split(hsv)
        hue_hist, bins = np.histogram(hue, 360)
        hues = {}

        i = 0
        while i < len(hue_color_name):
            if hue_color_name[i][2] in hues:
                hues[hue_color_name[i][2]] = hues.get(hue_color_name[i][2]) + np.sum(
                    hue_hist[hue_color_name[i][0]:hue_color_name[i][1]])
            else:
                hues[hue_color_name[i][2]] = (np.sum(hue_hist[hue_color_name[i][0]:hue_color_name[i][1]]))
            i += 1

        s_hues = sorted(hues, key=hues.get, reverse=True)
        return [s_hues[0], s_hues[1], s_hues[2]]

if __name__ == "__main__":
    initialization = Initialization().initialization()

