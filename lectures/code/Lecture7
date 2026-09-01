"""
The DuckDB half of the Spark comparison.

Builds the same table with the same number of rows as the Databricks notebook,
then runs the same query:

    SELECT venue, avg(price) FROM concerts GROUP BY venue

    pip install duckdb
    python duckdb_side.py
"""

import time

import duckdb

N_ROWS = 5_000_000        # must match N_ROWS in the notebook

VENUES = ["Debaser", "Fryshuset", "Nalen", "Slaktkyrkan", "Södra Teatern",
          "Annexet", "Avicii Arena", "Berns Salonger", "Cirkus",
          "Münchenbryggeriet", "Kägelbanan", "Klubben"]
GENRES = ["Pop", "Rock", "Hip-hop", "Electronic", "Indie", "Jazz", "Folk",
          "Metal", "Classical", "R&B"]

QUERY = "SELECT venue, avg(price) AS avg_price FROM concerts GROUP BY venue"


def build(con):
    con.execute(f"SET VARIABLE venues = {VENUES}")
    con.execute(f"SET VARIABLE genres = {GENRES}")
    t0 = time.perf_counter()
    con.execute(f"""
        CREATE OR REPLACE TABLE concerts AS
        SELECT
            i                                                               AS id,
            getvariable('venues')[floor(random() * {len(VENUES)})::INT + 1] AS venue,
            getvariable('genres')[floor(random() * {len(GENRES)})::INT + 1] AS genre,
            DATE '2015-01-01' + floor(random() * 4380)::INT                 AS date,
            round(random() * 1050 + 150, 2)                                 AS price
        FROM range({N_ROWS}) t(i)
    """)
    return time.perf_counter() - t0


def best_of(con, sql, repeats=3):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        con.execute(sql).fetchall()
        times.append(time.perf_counter() - t0)
    return times


def main():
    con = duckdb.connect()

    build_time = build(con)
    print(f"stored {N_ROWS:,} rows in {build_time:.1f}s")
    print(con.execute("SELECT * FROM concerts LIMIT 5").df().to_string(index=False))
    print()

    times = best_of(con, QUERY, repeats=4)
    first_run, rest = times[0], min(times[1:])

    print(f"first run      : {first_run:.3f}s")
    print(f"best of 3 more : {rest:.3f}s")
    print()
    print(con.execute(QUERY + " ORDER BY avg_price DESC").df().to_string(index=False))
    print()
    print(f"DUCKDB_SECONDS = {rest:.3f}      <- put this in the notebook")


if __name__ == "__main__":
    main()
