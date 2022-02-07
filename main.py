import requests
import sys
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('zadacha_design.ui', self)
        self.pushButton_4.clicked.connect(self.search)

    def search(self):
        zapros = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={self.lineEdit.text()}1&format=json"
        response = requests.get(zapros)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.lineEdit_2.setText(toponym_address + " имеет координаты:" + toponym_coodrinates)
            map_request = 'http://static-maps.yandex.ru/1.x/'
            params = {
                'll': ','.join(toponym_coodrinates.split(' ')),
                'l': 'map'
            }
            response = requests.get(map_request, params=params)
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap(self.map_file)
            self.image = self.label
            self.image.setPixmap(self.pixmap)
        else:
            print("Ошибка выполнения запроса:")
            print(zapros)
            print("Http статус:", response.status_code, "(", response.reason, ")")


    #
    # def getImage(self):
    #     map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
    #     response = requests.get(map_request)
    #
    #     if not response:
    #         print("Ошибка выполнения запроса:")
    #         print(map_request)
    #         print("Http статус:", response.status_code, "(", response.reason, ")")
    #         sys.exit(1)
    #     self.map_file = "map.png"
    #     with open(self.map_file, "wb") as file:
    #         file.write(response.content)
    #
    # def closeEvent(self, event):
    #     os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
