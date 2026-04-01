import psycopg2
dsn = b"host=localhost port=5432 dbname=postgres user=postgres password=postgres"
print("Тест подключения...")
conn = psycopg2.connect(dsn)
print("✅ PostgreSQL работает!")
conn.close()