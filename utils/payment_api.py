from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class PaymentApi(QObject):
    """Класс для взаимодействия с платёжной системой.
    Отправляет сигнал paymentResult(bool result)
    result - True при успешной оплате
    """

    paymentResult = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.timeout)

    def timeout(self):
        """Метод имитации оплаты (таймер 5 секунд)
        :return None:
        """
        self.paymentResult.emit(True)
        self.timer.stop()

    def start_pay(self, total: int) -> bool:
        """Метод начинает оплату.
        :param total:
        :return bool: Возвращает True при успехе
        """
        print("Оплата: ", total)
        self.timer.start()
        return True

    def cancel(self) -> bool:
        """Метод отменяет оплату.
        :return bool: Возвращает True при успехе
        """
        self.timer.stop()
        return True
