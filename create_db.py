import sqlite3

from const import MeasureUnit
from images_rep import IMAGES_PATH

SQL_SCRIPT_PATH = "./db_init"


class SqliteCm:
    def __init__(self, db_name):
        self.con = None
        self.db_name = db_name

    def __enter__(self):
        return self.open()

    def open(self):
        if not self.con:
            self.con = sqlite3.connect(self.db_name)
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.con:
            try:
                self.con.close()
            except Exception:
                pass
            self.con = False


def get_db():
    return SqliteCm("pizza_db.sqlite")


def create_db():
    with open(f"{SQL_SCRIPT_PATH}/create.sql", encoding="utf-8") as file:
        script = file.read()
    with get_db() as con:
        cur = con.cursor()
        cur.executescript(script)


def insert_data():
    with open(f"{SQL_SCRIPT_PATH}/initial_data.sql", encoding="utf-8") as file:
        script = file.read()

    with get_db() as con:
        cur = con.cursor()
        cur.executescript(script)


create_db()
insert_data()
