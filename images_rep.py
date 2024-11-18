from functools import cache

from PyQt6.QtGui import QPixmap

IMAGES_PATH = "./images/"

@cache
def get_pixmap(file_name: str) -> QPixmap:
    print(file_name)
    return QPixmap(IMAGES_PATH + file_name)