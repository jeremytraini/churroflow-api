import psycopg2

# Connect to PostgreSQL as default user 'postgres'
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Create a new database called 'validation'
cur = conn.cursor()
cur.execute("CREATE DATABASE validation;")
conn.commit()
conn.close()
