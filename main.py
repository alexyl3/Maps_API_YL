import sys
from map import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from io import BytesIO
import requests
from PIL import Image, ImageQt


class Menu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.lon = "37.564985"
        self.lat = "55.725680"
        self.delta = "0.002"
        self.lt = "map"
        self.pt = None
        self.upd()
        Image.open(BytesIO(self.response.content)).save('map.png')
        self.pix = QPixmap('map.png')
        self.label.setPixmap(self.pix)
        self.pushButton.clicked.connect(self.scale_up)
        self.pushButton_2.clicked.connect(self.scale_down)
        self.pushButton_3.clicked.connect(self.map)
        self.pushButton_4.clicked.connect(self.sat)
        self.pushButton_5.clicked.connect(self.skl)
        self.pushButton_6.clicked.connect(self.search)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

    def scale_up(self):
        if float(self.delta) > 0.0001:
            self.delta = str(float(self.delta) * 2)
        self.upd()

    def scale_down(self):
        if float(self.delta) < 1:
            self.delta = str(float(self.delta) * 0.5)
        self.upd()

    def upd(self):
        self.params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": self.lt,
            "pt": self.pt
        }
        self.response = requests.get(self.api_server, params=self.params)
        self.img = ImageQt.ImageQt(Image.open(BytesIO(self.response.content)))
        self.pix = QPixmap('map.png')
        self.label.setPixmap(QPixmap.fromImage(self.img))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A or event.key() == 1060:
            self.move([0, -1])
        elif event.key() == Qt.Key_D or event.key() == 1042:
            self.move([0, 1])
        elif event.key() == Qt.Key_S or event.key() == 1067:
            self.move([-1, 0])
        elif event.key() == Qt.Key_W or event.key() == 1062:
            self.move([1, 0])

    def mousePressEvent(self, event):
        # (340, 20, 190, 21)
        if 340 <= event.x() <= 530 and 20 <= event.y() <= 41:
            self.lineEdit.setDisabled(False)
            self.lineEdit.setFocus()
        else:
            self.lineEdit.setDisabled(True)

    def move(self, dist):
        self.lon = str(float(self.lon) + dist[1] * float(self.delta) * 3.2)
        self.lat = str(float(self.lat) + dist[0] * float(self.delta) * 1.32)
        self.upd()

    def map(self):
        self.lt = "map"
        self.upd()

    def sat(self):
        self.lt = "sat"
        self.upd()

    def skl(self):
        self.lt = "skl"
        self.upd()

    def search(self):
        toponym_to_find = self.lineEdit.text()
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        geo_response = requests.get(self.geocoder_api_server, params=geocoder_params)
        json_response = geo_response.json()
        if json_response["response"]["GeoObjectCollection"]["featureMember"]:
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.lon, self.lat = toponym_coodrinates.split(" ")
            self.pt = "{0},pm2ntl".format("{0},{1}".format(self.lon, self.lat))
            self.upd()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
