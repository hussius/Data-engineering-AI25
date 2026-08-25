import os
import time

import duckdb

from dotenv import load_dotenv

load_dotenv()

cs = os.environ["CONN_STR"]
con = duckdb.connect()
con.sql("INSTALL postgres; LOAD postgres;")
con.sql(f"""
    ATTACH '{cs}'
    AS concerts (TYPE postgres)
""")

# via DuckDB, same query, same table

t0 = time.perf_counter()
con.sql("""
    SELECT city, genre, count(*), avg(price)
    FROM concerts.synthetic_events
    GROUP BY city, genre
    ORDER BY count(*) DESC
""").show()
print(f"{time.perf_counter() - t0:.2f}s")
