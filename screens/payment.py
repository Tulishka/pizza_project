from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSpacerItem, QSizePolicy

import state
from payment_api import PaymentApi
from screens.base import BaseScreen


class PaymentWidget(BaseScreen):
    """Экран оплаты"""

    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                font-size: 30pt;
            }
        """)

        self.paymentApi = PaymentApi(self)
        self.paymentApi.paymentResult.connect(self.pay_done)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setSpacing(24)

        self.price = QLabel(f"Оплатите 0 ₽", self)
        self.label = QLabel("Следуйте указаниям\nна терминале оплаты", self)

        self.vlayout.addWidget(self.price, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addSpacerItem(QSpacerItem(1, 100, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))

    def activated(self):
        """Обработчик открытия экрана оплаты: показывает сумму и запускает оплату через API платёжной системы
        :return None:
        """
        self.price.setText(f"Оплатите {state.State.order.total_sum} ₽")
        self.paymentApi.start_pay(state.State.order.total_sum)

    def pay_done(self, result: bool):
        """Обработчик ответа платёжной системы
        :param result: bool - True если платёж успешно выполнен
        :return None:
        """
        if result:
            self.next.emit()

    def prev_clicked(self):
        """Обработчик кнопки назад, отменяется оплата, и используется действие по умолчанию
        :return None:
        """
        self.paymentApi.cancel()
        super().prev_clicked()
