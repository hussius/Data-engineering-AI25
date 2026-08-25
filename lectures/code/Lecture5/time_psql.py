import os
import time

import psycopg2

from dotenv import load_dotenv

load_dotenv()

cs = os.environ["CONN_STR"]
conn = psycopg2.connect(cs)
cur = conn.cursor()

# via psql/Postgres itself, same query, same table -- the aggregation runs
# inside Neon's compute, right next to the data; only the small result set
# (one row per city/genre pair) travels back over the network

t0 = time.perf_counter()
cur.execute("""
    SELECT city, genre, count(*), avg(price)
    FROM synthetic_events
    GROUP BY city, genre
    ORDER BY count(*) DESC
""")
rows = cur.fetchall()
elapsed = time.perf_counter() - t0

for row in rows:
    print(row)
print(f"{elapsed:.2f}s")

cur.close()
conn.close()
