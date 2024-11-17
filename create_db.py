import sqlite3

from const import MeasureUnit


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
    with get_db() as con:
        cur = con.cursor()

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title  TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            serving_size INTEGER NOT NULL,
            measure_unit TEXT NOT NULL DEFAULT 'шт.',
            price INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            count INTEGER NOT NULL DEFAULT 10
        );
        """)


def insert_data():
    with get_db() as con:
        cur = con.cursor()
        text = f"""
            INSERT OR IGNORE INTO categories (id, title) VALUES (1, 'Овощи'), (2, 'Мясо'), (3, 'Сыр');
            
            INSERT OR IGNORE INTO ingredients (name,title,serving_size,measure_unit,price,category_id,weight)
                VALUES 
                ('mozzarella','Моцарелла', 4, '{MeasureUnit.PIECES}', 89, 3, 40),
                ('olive','Оливки', 8, '{MeasureUnit.PIECES}', 69, 1, 24),
                ('pepperoni','Пепперони', 6, '{MeasureUnit.PIECES}', 89, 2, 48),
                ('pineapple','Ананас', 7, '{MeasureUnit.PIECES}', 69, 1, 56),
                ('shrimp_royal','Королевские креветки', 3, '{MeasureUnit.PIECES}', 189, 2, 75),
                ('shrimp','Креветки', 5, '{MeasureUnit.PIECES}', 119, 2, 50),
                ('tomato','Томаты', 6, '{MeasureUnit.PIECES}', 79, 1, 60)
           """
        cur.executescript(text)

create_db()
insert_data()
