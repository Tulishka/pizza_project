from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSpacerItem,
    QSizePolicy, QHBoxLayout, QButtonGroup, QMessageBox
)

PIZZA_DOUGHS = ["Традиционная", "Тонкое тесто"]
PIZZA_SIZES = [25, 30, 35, 40]
PIZZA_SOUSES = ["Томатный", "Сливочный"]

class PizzaBaseWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(self.parent().width(), self.parent().height())

        self.next = None

        self.setStyleSheet("""
            QWidget { border-radius: 16px; }
            
            QPushButton {
                background-color: #ECECEC;
                border: 2px solid #00000000;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
            }        
            QPushButton:hover {
                border-color: #555555;
            } 
            
            QPushButton:checked {
                border: 2px solid #333333;
            }
            
            #dough {
                font-size: 32px;
                background-color: #D9CAA0;
            } 
                        
            #size {
                font-size: 16px;
                background-color: #ECECEC;
            } 
            
            #souses {
                font-size: 20px;
                background-color: #ECECEC;
            } 

            #okButton {
                font-size: 20px;
                background-color: #6CE08F;
            }             
            
        """)

        self.back = QWidget(self)
        self.back.resize(1024, 768)
        self.back.move(0, 0)
        self.back.setStyleSheet("""
            background-color: #555555;
            border-radius: 0;
        """)


        self.hlayout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout(self)

        self.hlayout.setContentsMargins(0, 0, 0, 0)

        self.hlayout.addLayout(self.vlayout)
        self.widget = QWidget(self)
        self.widget.setMaximumSize(500, 390)
        self.widget.setObjectName("centralWidget")

        self.vlayout.addWidget(self.widget)
        self.widget_layout = QVBoxLayout(self.widget)
        self.widget_layout.setSpacing(12)
        self.widget.setContentsMargins(8,8,8,8)
        self.heading = QLabel("Выберите основу пиццы:", self)
        font = QFont()
        font.setPointSize(20)
        self.heading.setFont(font)
        self.widget_layout.addWidget(self.heading)

        self.dough_layout = QHBoxLayout(self)
        self.dough_group = QButtonGroup(self)
        self.dough_layout.setObjectName("dough_group")

        for name in PIZZA_DOUGHS:
            button = QPushButton(name, self)
            button.setObjectName("dough")
            button.setCheckable(True)
            self.dough_layout.addWidget(button)
            self.dough_group.addButton(button)

        self.size_layout = QHBoxLayout(self)
        self.size_group = QButtonGroup(self)
        for size in PIZZA_SIZES:
            button = QPushButton(f'{size} см.', self)
            button.setObjectName("size")
            button.pizza_size = size
            button.setCheckable(True)
            self.size_layout.addWidget(button)
            self.size_group.addButton(button)

        self.souse_label = QLabel("Выбери соус:", self)
        font = QFont()
        font.setPointSize(14)
        self.souse_label.setFont(font)

        self.souse_layout = QHBoxLayout(self)
        self.souse_group = QButtonGroup(self)
        for name in PIZZA_SOUSES:
            button = QPushButton(name, self)
            button.setObjectName("souse")
            button.setCheckable(True)
            self.souse_layout.addWidget(button)
            self.souse_group.addButton(button)


        self.widget_layout.addLayout(self.dough_layout)
        self.widget_layout.addLayout(self.size_layout)
        self.widget_layout.addWidget(self.souse_label)
        self.widget_layout.addLayout(self.souse_layout)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setMaximumWidth(100)
        self.ok_button.setMinimumWidth(100)
        self.ok_button.clicked.connect(self.ok_click)
        self.ok_button.setObjectName("okButton")


        self.widget_layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)

    def ok_click(self):
        dough = self.dough_group.checkedButton()
        size = self.size_group.checkedButton()
        souse = self.souse_group.checkedButton()

        if not dough or not size or not souse:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Ваша пицца")
            msg_box.setText("Для продолжения необходимо сделать выбор в каждой категории")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            msg_box.exec()
            return

        self.next()
