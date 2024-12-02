"""Файл содержит функции для создания БД и её наполнения начальными данными"""

import const
from utils.sqllite_cm import SqliteCm

SQL_SCRIPT_PATH = const.APP_DIR + "db_init"


def get_db() -> SqliteCm:
    """Функция для получения соединения с БД
    :return SqliteCm: Контекстный менеджер для работы с соединением
    """

    return SqliteCm("pizza_db.sqlite")


def create_db():
    """Создание таблиц БД
    :return None:
    """

    with open(f"{SQL_SCRIPT_PATH}/create.sql", encoding="utf-8") as file:
        script = file.read()

    with get_db() as con:
        cur = con.cursor()
        cur.executescript(script)


def insert_data():
    """Вставка начальных данных в БД
    :return:
    """

    with open(f"{SQL_SCRIPT_PATH}/initial_data.sql", encoding="utf-8") as file:
        script = file.read()

    with get_db() as con:
        cur = con.cursor()
        cur.executescript(script)


create_db()
insert_data()
