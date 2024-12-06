from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

from PyQt6.QtWidgets import QPushButton


class PizzaButton(QPushButton):
    """Кнопка со звуком"""
    button_sound: QSoundEffect = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if PizzaButton.button_sound is None:
            PizzaButton.button_sound = QSoundEffect()
            PizzaButton.button_sound.setSource(QUrl.fromLocalFile("sounds/pop.wav"))

        self.clicked.connect(self.play_sound)

    def play_sound(self):
        self.button_sound.play()
