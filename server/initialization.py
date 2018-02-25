# coding: utf8
import sqlite3
import os
import random
import cv2
import numpy as np

path_to_hairstyles = './hairstyle_images'
path_to_men_hairstyles = "/men"
path_to_women_hairstyles = "/women"

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

def initialization():
    # Установка соединения и назначение курсора
    connection = sqlite3.connect('./database/main_db.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM hairstyle_images")

    print("Сканирование женских шаблонов...")

    dir_and_subdir_templates = [
        os.path.join(path_to_hairstyles+path_to_women_hairstyles, name)
        for dir_path, dirs, files in os.walk(path_to_hairstyles+path_to_women_hairstyles)
        for name in files
        if name.endswith((".jpg", ".png", ".jpeg"))
    ]

    print(dir_and_subdir_templates)


    hair_types = ["normal", "greasy", "dry", "mixed"]
    i = 0
    for template in dir_and_subdir_templates:
        #hair_type = input("Введите тип волос (normal, greasy, dry, mixed): ")
        #while hair_type not in hair_types:
        #    print("Ошибка: вы можете ввести только значения: normal, greasy, dry, mixed")
        #    hair_type = input("Введите тип волос (normal, greasy, dry, mixed): ")
        hair_type = random.choice(hair_types)
        length = detect_hair_length(template)
        color = detect_primary_color(template)
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


def detect_hair_length(single_template):
    single_template = cv2.imread(single_template)
    length = None
    for item in hair_length_associate:
        if hair_length_associate.get(item)['min'] <= int(single_template.shape[0]) <= hair_length_associate.get(item)['max']:
            length = item
    return length

def detect_primary_color(single_template):
    pass

def remove_background():
    dir_and_subdir_templates = convert_to_png()

    for template in dir_and_subdir_templates:
        src = cv2.imread(template, 1)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        _, alpha = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        cv2.imwrite(template, dst)


def convert_to_png():
    dir_and_subdir_templates = [
        os.path.join(path_to_hairstyles + path_to_women_hairstyles, name)
        for dir_path, dirs, files in os.walk(path_to_hairstyles + path_to_women_hairstyles)
        for name in files
        if name.endswith((".jpg", ".png", ".jpeg"))
    ]

    for template in dir_and_subdir_templates:
        src = cv2.imread(template)

        cv2.imwrite(template[:-3] + 'png', src)
        os.remove(template)

    dir_and_subdir_templates = [
        os.path.join(path_to_hairstyles + path_to_women_hairstyles, name)
        for dir_path, dirs, files in os.walk(path_to_hairstyles + path_to_women_hairstyles)
        for name in files
        if name.endswith(".png")
    ]

    return dir_and_subdir_templates

if __name__ == "__main__":
    initialization()
