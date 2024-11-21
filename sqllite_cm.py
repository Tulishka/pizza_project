import sqlite3


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
