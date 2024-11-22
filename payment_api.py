from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class PaymentApi(QObject):
    paymentResult = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.timeout)

    def timeout(self):
        self.paymentResult.emit(True)
        self.timer.stop()

    def start_pay(self, total: int) -> bool:
        print("Оплата: ", total)
        self.timer.start()
        return True

    def cancel(self) -> bool:
        self.timer.stop()
        return True
