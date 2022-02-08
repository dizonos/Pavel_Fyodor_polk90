import requests
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('zadacha_design.ui', self)
        self.pushButton_4.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.sat)
        self.pushButton_3.clicked.connect(self.gibr)
        self.pushButton.clicked.connect(self.map)
        self.view = 'map'
        self.z = 10

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_PageUp:
            self.z += 1
            if self.z > 17:
                self.z = 17
            self.search()
        elif e.key() == Qt.Key_PageDown:
            self.z -= 1
            if self.z < 0:
                self.z = 0
            self.search()

    def search(self):
        zapros = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={self.lineEdit.text()}1&format=json"
        response = requests.get(zapros)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.textEdit.setPlainText(toponym_address + " имеет координаты: \n" + toponym_coodrinates)
            map_request = 'http://static-maps.yandex.ru/1.x/'
            params = {
                'll': ','.join(toponym_coodrinates.split(' ')),
                'z': str(self.z),
                'l': self.view,
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

    def sat(self):
        self.view = 'sat'

    def gibr(self):
        self.view = 'skl'

    def map(self):
        self.view = 'map'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
