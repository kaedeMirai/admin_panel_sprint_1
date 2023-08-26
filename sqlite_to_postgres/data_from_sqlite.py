import sqlite3
from dataclasses import fields
from contextlib import contextmanager


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def data_from_sqlite(db_path, table_name, dataclass):
    try:
        with conn_context(db_path) as conn:
            curs = conn.cursor()
            curs.execute(f"""SELECT * FROM {table_name};""")
            data = curs.fetchall()

            column_names = [field.name for field in fields(dataclass)]
            return data, column_names

    except sqlite3.Error as ex:
        print("Ошибка при чтении данных из SQLite:", ex)
