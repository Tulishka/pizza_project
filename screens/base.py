from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton


class BaseScreen(QWidget):
    next = pyqtSignal()
    prev = pyqtSignal()

    def activated(self):
        pass

    def setup_prev_button(self, prev_button: QPushButton):
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
        self.prev.emit()
