import sys
from map import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from io import BytesIO
import requests
from PIL import Image


class Menu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = "37.564985"
        lat = "55.725680"
        delta = "0.002"
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)
        Image.open(BytesIO(response.content)).save('map.png')
        self.pix = QPixmap('map.png')
        self.label.setPixmap(self.pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
