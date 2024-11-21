from utils.sqllite_cm import SqliteCm

SQL_SCRIPT_PATH = "./db_init"


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
