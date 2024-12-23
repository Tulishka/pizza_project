"""Функции для получения и кэширования картинок"""

from functools import cache

from PyQt6.QtGui import QPixmap, QImage

from utils import const

IMAGES_PATH = const.APP_DIR + "images/"

@cache
def get_pixmap(file_name: str) -> QPixmap:
    return QPixmap(IMAGES_PATH + file_name)


@cache
def get_image(file_name: str) -> QImage:
    return QImage(IMAGES_PATH + file_name)
