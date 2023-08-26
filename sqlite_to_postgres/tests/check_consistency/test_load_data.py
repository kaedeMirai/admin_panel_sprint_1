import unittest
import sqlite3
import psycopg2

# Подключение к базам данных

psql_conn_data = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': 'localhost',
    'port': 54320,
    'options': '-c search_path=content',
    'client_encoding': 'utf-8',
}

db_sqlite_path = r'./sqlite_to_postgres/db.sqlite'
sqlite_conn = sqlite3.connect(db_sqlite_path)
pg_conn = psycopg2.connect(**psql_conn_data)


class TestDatabaseMigration(unittest.TestCase):

    tables_to_check = ['genre', 'film_work', 'person', 'genre_film_work', 'person_film_work']

    def test_record_counts(self):
        # Проверка количества записей между SQLite и PostgreSQL

        for table in self.tables_to_check:
            sqlite_cursor = sqlite_conn.cursor()
            pg_cursor = pg_conn.cursor()

            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table};")
            pg_cursor.execute(f"SELECT COUNT(*) FROM content.{table};")

            sqlite_count = sqlite_cursor.fetchone()[0]
            pg_count = pg_cursor.fetchone()[0]

            self.assertEqual(sqlite_count, pg_count, f"Количество записей в таблице {table} не совпадает.")

    def test_record_contents(self):
        # Проверка равенства полей записи между sqlite и postgresql
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()

        for table in self.tables_to_check:
            sqlite_cursor.execute(f"SELECT * FROM {table};")
            sqlite_records = sqlite_cursor.fetchall()
            print(sqlite_records[0])
            pg_cursor.execute(f"SELECT * FROM content.{table};")
            pg_records = pg_cursor.fetchall()
            print(pg_records[0])

            self.assertCountEqual(sqlite_records, pg_records, f"Содержимое записей в таблице {table} не совпадает.")

    def test_table_existence(self):
        # Проверка наличия таблиц в PostgreSQL
        pg_cursor = pg_conn.cursor()

        expected_tables = ['genre', 'film_work', 'person', 'genre_film_work', 'person_film_work']

        pg_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'content';")

        pg_tables = [record[0] for record in pg_cursor.fetchall()]

        for table in expected_tables:
            self.assertIn(table, pg_tables, f"Таблица {table} отсутствует в PostgreSQL.")


if __name__ == '__main__':
    unittest.main()
