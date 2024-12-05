import csv
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QStackedLayout, QSizePolicy, QPushButton, QHBoxLayout, QTableView, QTabWidget,
    QToolBar, QFileDialog, QMessageBox
)
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase

import database.create_db
from utils import const


class PizzaTechnolog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Редактирование ингредиентов')
        self.setGeometry(300, 150, const.MAIN_WINDOW_WIDTH, const.MAIN_WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white")
        # self.setFixedSize(const.MAIN_WINDOW_WIDTH, const.MAIN_WINDOW_HEIGHT)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("pizza_db.sqlite")

        ingredients_model = QSqlTableModel()
        ingredients_model.setTable("ingredients")
        ingredients_model.select()

        souses_model = QSqlTableModel()
        souses_model.setTable("souses")
        souses_model.select()

        models = [
            ('Ингредиенты', ingredients_model), ('Соусы', souses_model),
        ]

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.toolbar = QToolBar(self)
        self.vlayout.addWidget(self.toolbar)

        buttons = [
            ("Добавить нов.", self.add_row),
            ("Удалить строки", self.delete_rows),
            ("Загрузить из CSV", self.load_from_cvs),
            ("Сохранить в CVS", self.save_to_cvs),
        ]

        for title, func in buttons:
            btn = QPushButton(title, self)
            btn.clicked.connect(func)
            self.toolbar.addWidget(btn)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        for title, model in models:
            tab = QTableView(self)
            tab.resize(self.width(), self.height())
            tab.setModel(model)
            tab.setEditTriggers(
                QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.EditKeyPressed
            )
            tab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.tab_widget.addTab(tab, title)

        self.vlayout.addWidget(self.tab_widget)

    def current_model(self) -> QSqlTableModel:
        return self.tab_widget.currentWidget().model()

    def current_view(self) -> QTableView:
        return self.tab_widget.currentWidget()

    def add_row(self):
        self.current_model().insertRow(self.current_model().rowCount())

    def delete_rows(self):
        model = self.current_model()
        selected_indexes = self.current_view().selectionModel().selectedRows()
        for index in sorted(selected_indexes):
            model.removeRow(index.row())
        model.submitAll()
        model.select()

    def load_from_cvs(self):
        model = self.current_model()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Загрузить из CSV", "", "CSV файлы (*.csv);;Все файлы (*)"
        )
        if file_name:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                model.removeRows(0, model.rowCount())
                for row in reader:
                    model.insertRow(model.rowCount())
                    for column, value in enumerate(row):
                        if column != 0:
                            model.setData(model.index(model.rowCount() - 1, column), value)
                    model.submitAll()

            model.select()

    def save_to_cvs(self):
        model = self.current_model()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить в CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                headers = [model.headerData(i, Qt.Orientation.Horizontal) for i in range(model.columnCount())]
                writer.writerow(headers)
                for row in range(model.rowCount()):
                    row_data = []
                    for column in range(model.columnCount()):
                        row_data.append(model.data(model.index(row, column)))
                    writer.writerow(row_data)


def exception_logger(*args):
    print(*args)
    sys.__excepthook__(*args)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_logger
    ex = PizzaTechnolog()
    ex.show()
    sys.exit(app.exec())
