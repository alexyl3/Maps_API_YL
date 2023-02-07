import sys
from map import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from io import BytesIO
import requests
from PIL import Image


class Menu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.lon = "37.564985"
        self.lat = "55.725680"
        self.delta = "0.002"
        self.lt = "map"
        self.upd()
        Image.open(BytesIO(self.response.content)).save('map.png')
        self.pix = QPixmap('map.png')
        self.label.setPixmap(self.pix)
        self.pushButton.clicked.connect(self.scale_up)
        self.pushButton_2.clicked.connect(self.scale_down)
        self.pushButton_3.clicked.connect(self.map)
        self.pushButton_4.clicked.connect(self.sat)
        self.pushButton_5.clicked.connect(self.skl)

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
            "l": self.lt
        }
        self.response = requests.get(self.api_server, params=self.params)
        Image.open(BytesIO(self.response.content)).save('map.png')
        self.pix = QPixmap('map.png')
        self.label.setPixmap(self.pix)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.move([0, -1])
        elif event.key() == Qt.Key_D:
            self.move([0, 1])
        elif event.key() == Qt.Key_S:
            self.move([-1, 0])
        elif event.key() == Qt.Key_W:
            self.move([1, 0])

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
