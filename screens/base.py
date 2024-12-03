from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton


class BaseScreen(QWidget):
    """Базовый класс для экранов"""

    next = pyqtSignal()
    prev = pyqtSignal()

    def activated(self):
        """Обработчик открытия экрана по умолчанию (вызывается при переходе на экран)
        :return None:
        """
        pass

    def setup_prev_button(self, prev_button: QPushButton):
        """Настройка кнопки назад для экранов
        :param prev_button:
        :return None:
        """

        prev_button.setText("< Назад")
        prev_button.setStyleSheet("""
            QPushButton {
                color: #3D3D3D;
                background-color: #CFCFCF;
                border: 2px solid #00000000;
                border-radius: 15px;
                padding: 10px;
                font-size: 22px;
                z-index:100;
            }        
            
            QPushButton:hover {
                border-color: #555555;
            }
        """)

    def prev_clicked(self):
        """Вызывается при нажатии кнопки назад, по умолчанию отправляет сигнал prev
        :return None:
        """

        self.prev.emit()
