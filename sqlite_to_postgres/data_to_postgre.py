import psycopg2


def insert_data_to_postgres(data, table_name, column_names, psql_conn_data):
    try:
        with psycopg2.connect(**psql_conn_data) as conn, conn.cursor() as cursor:
            # cursor.execute(f"""TRUNCATE content.{table_name}""")
            col_count = ', '.join(['%s'] * len(column_names))
            query_insert = f"""
                INSERT INTO content.{table_name} ({", ".join(column_names)})
                VALUES ({col_count})
                ON CONFLICT (id) DO NOTHING
                """
            for item in data:
                cursor.execute(query_insert, item)

    except psycopg2.Error as ex:
        print("Ошибка при записи данных в postgreSQL:", ex)
