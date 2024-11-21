import sqlite3

from const import MeasureUnit
from images_rep import IMAGES_PATH


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
            count INTEGER NOT NULL DEFAULT 10,
            auto_place_method TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS dought_types (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            unit_weight REAL NOT NULL,
            img TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS souses (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            unit_weight REAL NOT NULL,
            img TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS pizzas (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dough_type_id INTEGER NOT NULL,
            souse_id INTEGER NOT NULL,
            size INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS pizzas_ingredients (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            pizza_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            addition_order INTEGER NOT NULL,
            count INTEGER NOT NULL,
            portion_size INTEGER NOT NULL,
            position TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            pizza_id INTEGER NOT NULL,
            status TEXT NOT NULL
        );     
           
        CREATE TABLE IF NOT EXISTS base_prices (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dought_tipe_id INTEGER NOT NULL,
            souse_id INTEGER NOT NULL,
            size INTEGER NOT NULL,
            price INTEGER NOT NULL,
            UNIQUE (dought_tipe_id,souse_id,size)
        );
          
        """)


def insert_data():
    with get_db() as con:
        cur = con.cursor()
        text = f"""
            INSERT OR IGNORE INTO categories (id, title) VALUES (1, 'Овощи'), (2, 'Мясо'), (3, 'Сыр');
            
            INSERT OR IGNORE INTO ingredients (name,title,serving_size,measure_unit,price,category_id,weight, auto_place_method)
                VALUES 
                ('mozzarella','Моцарелла', 4, '{MeasureUnit.PIECES}', 89, 3, 40, 'circle'),
                ('mozzarella_mini','Моцарелла мини', 6, '{MeasureUnit.PIECES}', 89, 3, 39, 'random'),
                ('olive','Оливки', 8, '{MeasureUnit.PIECES}', 69, 1, 24, 'random'),
                ('pepperoni','Пепперони', 6, '{MeasureUnit.PIECES}', 89, 2, 48, 'mosaic'),
                ('pineapple','Ананасы', 7, '{MeasureUnit.PIECES}', 69, 1, 56, 'random'),
                ('shrimp_royal','Королевские креветки', 3, '{MeasureUnit.PIECES}', 189, 2, 75, 'circle'),
                ('shrimp','Креветки', 5, '{MeasureUnit.PIECES}', 119, 2, 50, 'circle'),
                ('sweet_pepper','Сладкий перец', 3, '{MeasureUnit.PIECES}', 79, 1, 110, 'mosaic'),
                ('pickled_cucumbers','Маринованные огурцы', 6, '{MeasureUnit.PIECES}', 79, 1, 29, 'random'),
                ('oregano','Орегано', 5, '{MeasureUnit.PIECES}', 79, 1, 18, 'random'),
                ('onion','Лук', 5, '{MeasureUnit.PIECES}', 79, 1, 38, 'random'),
                ('jalapeno_pepper','Перец халапеньо', 6, '{MeasureUnit.PIECES}', 79, 1, 35, 'random'),
                ('ham','Ветчина', 5, '{MeasureUnit.PIECES}', 89, 2, 125, 'circle'),
                ('garlic','Чеснок', 8, '{MeasureUnit.PIECES}', 69, 1, 28, 'random'),
                ('chicken_breast','Куринная грудка', 4, '{MeasureUnit.PIECES}', 89, 2, 128, 'circle'),
                ('cheddar_cheese','Сыр чеддер', 4, '{MeasureUnit.PIECES}', 89, 3, 79, 'circle'),
                ('champignons','Шампиньоны', 6, '{MeasureUnit.PIECES}', 69, 1, 65, 'random'),
                ('bacon','Бекон', 5, '{MeasureUnit.PIECES}', 89, 2, 48, 'circle'),
                ('tomato','Томаты', 5, '{MeasureUnit.PIECES}', 79, 1, 130, 'circle');
                                       
            INSERT OR IGNORE INTO dought_types (id, title, unit_weight, img) 
                VALUES 
                (1, 'Традиционная', 1, 'pizza_big_base.png'), 
                (2, 'Тонкое тесто', 0.9, 'pizza_small_base.png');
                        
            INSERT OR IGNORE INTO souses (id, title, unit_weight, img)
                VALUES 
                (1, 'Томатный', 1, 'tomato_souse.png'), 
                (2, 'Сливочный', 1, 'creamy_souse.png');
                       
            INSERT OR IGNORE INTO base_prices (dought_tipe_id, souse_id, size, price)
                VALUES 
                (1, 1, 25, 419),
                (1, 2, 25, 419),
                (2, 1, 25, 419),
                (2, 2, 25, 419),
                (1, 1, 30, 569),
                (1, 2, 30, 569),
                (2, 1, 30, 569),
                (2, 2, 30, 569),
                (1, 1, 35, 719),
                (1, 2, 35, 719),
                (2, 1, 35, 719),
                (2, 2, 35, 719),
                (1, 1, 40, 869),
                (1, 2, 40, 869),
                (2, 1, 40, 869),
                (2, 2, 40, 869)
                
            
           """
        cur.executescript(text)


create_db()
insert_data()
