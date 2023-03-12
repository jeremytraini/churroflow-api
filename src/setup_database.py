import psycopg2
import os

conn = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    database=os.environ['POSTGRES_DB']
)

cur = conn.cursor()
cur.execute('SELECT * FROM Reports')
rows = cur.fetchall()
print(rows)

conn.close()
