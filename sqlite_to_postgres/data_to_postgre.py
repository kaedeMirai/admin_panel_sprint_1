import logging
import psycopg2


logging.basicConfig(level=logging.ERROR)


def insert_data_to_postgres(data, table_name, column_names, psql_conn_data):
    try:
        with psycopg2.connect(**psql_conn_data) as conn, conn.cursor() as cursor:
            col_count = ', '.join(['%s'] * len(column_names))
            args = ','.join(cursor.mogrify(f"({col_count})", item1).decode() for item1 in data)
            query_insert = f"""
                INSERT INTO content.{table_name} ({", ".join(column_names)})
                VALUES {args}
                ON CONFLICT (id) DO NOTHING
                """
            cursor.execute(query_insert)

    except psycopg2.Error as ex:
        logging.error("Ошибка при записи данных в postgreSQL:", ex)
