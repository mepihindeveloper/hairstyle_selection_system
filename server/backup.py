import os
import shutil
import zipfile
import datetime


'''
    Класс для работы с функцией резервирования и восстановления системы
'''


class BackUp:
    def __init__(self):
        self.params = {
            'period_hours': 168,
            'folder': '../backups/',
            'archive_files': {
                'client': {
                    'name': 'client.zip',
                    'folder': '../client/'
                },
                'server': {
                    'name': 'server.zip',
                    'folder': '../server/'
                }
            }
        }


    def zipdir(self, path, ziph):
        # ziph - zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    # Функция для создания архива с параметрами
    def make_zip(self, goal="all"):
        '''
        :param goal: цель (что архивировать)
        :return:
        '''
        prefix = self.params.get("folder")+"{}-{}-{}_".format(
            datetime.datetime.now().year,
            datetime.datetime.now().month,
            datetime.datetime.now().day
        )
        if goal is "all":
            for item in self.params.get("archive_files"):
                zipf = zipfile.ZipFile(
                    prefix+self.params.get("archive_files").get(item).get("name"),
                    'w',
                    zipfile.ZIP_DEFLATED
                )
                self.zipdir(self.params.get("archive_files").get(item).get("folder"), zipf)
                zipf.close()
        else:
            zipf = zipfile.ZipFile(
                prefix + self.params.get("archive_files").get(goal).get("name"),
                'w',
                zipfile.ZIP_DEFLATED
            )
            self.zipdir(self.params.get("archive_files").get(goal).get("folder"), zipf)
            zipf.close()

    # Функция удаления папки, перед восстановлением
    def clear_dir(self, dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)

    # Восстановленеи из архива
    def restore(self, archive, goal):
        '''
        :param archive: Имя архива
        :param goal: цель (какой тип имеет объект восстановления (фото, сервер или клиент))
        :return:
        '''
        folder = self.params.get("archive_files").get(goal).get("folder")
        archive = self.params.get("folder")+archive

        zipf = zipfile.ZipFile(archive, 'r')
        zipf.extractall("../")
        zipf.close()


if __name__ == '__main__':
    BackUp().make_zip(goal="server")
    #BackUp().clear_dir("./hairstyle_images")
    #BackUp().restore("2018-3-10_hairstyle_images.zip", 'hairstyle_images')
    #pass