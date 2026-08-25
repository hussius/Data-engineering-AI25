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

# Step 1: materialize a local copy. This pulls all ~1M rows across the
# network ONCE and stores them in DuckDB's own columnar format on this
# machine. This is the cost the naive ATTACH-and-query approach pays on
# EVERY query -- here we pay it a single time, up front.

t0 = time.perf_counter()
con.sql("""
    CREATE OR REPLACE TABLE local_events AS
    SELECT * FROM concerts.synthetic_events
""")
copy_time = time.perf_counter() - t0
print(f"one-time materialize (network copy): {copy_time:.2f}s")

# Step 2: query the local copy. No network round-trip left at all -- this
# is DuckDB doing what it's built for, a columnar scan entirely on local
# disk/memory. Run it more than once if you want to show it stays fast on
# repeat queries, which is the realistic case for a team iterating on the
# same dataset all afternoon.

t0 = time.perf_counter()
con.sql("""
    SELECT city, genre, count(*), avg(price)
    FROM local_events
    GROUP BY city, genre
    ORDER BY count(*) DESC
""").show()
query_time = time.perf_counter() - t0
print(f"local query (after materialize): {query_time:.2f}s")
print(f"total (materialize + first query): {copy_time + query_time:.2f}s")
