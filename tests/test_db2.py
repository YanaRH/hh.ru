import psycopg2
import os

# Очищаем окружение
os.environ.pop('PGPASSWORD', None)

conn_params = {
    "host": "localhost",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "connect_timeout": 10,
    "options": "-c client_encoding=utf8"
}

try:
    print("Попытка подключения...")
    conn = psycopg2.connect(**conn_params)
    print("Успешное подключение!")
    conn.close()
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()