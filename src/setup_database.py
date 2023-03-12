import psycopg2

# Connect to PostgreSQL as default user 'postgres'
try:
    connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE validation")
finally:
    if connection:
        connection.close()
