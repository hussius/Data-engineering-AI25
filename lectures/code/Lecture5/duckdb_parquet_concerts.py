import time

import duckdb

input("Press to show first 5 from CSV file:\n")
query_str_csv = "SELECT * FROM 'concerts.csv' LIMIT 5";
response = duckdb.sql(query_str_csv)
print(response)


input("Press to show average price from CSV file:\n")
query_str_agg = "SELECT venue, avg(price) FROM 'concerts.csv' GROUP BY venue;"
t1 = time.time()
response = duckdb.sql(query_str_agg)
t2 = time.time()
print(response)
td = t2-t1
print(f'Time taken: {td:2f}')

input("Press to show first 5 from Parquet file:\n")
query_str_csv = "SELECT * FROM 'concerts.parquet' LIMIT 5";
response = duckdb.sql(query_str_csv)
print(response)

input("Press to show average price from Parquet file:\n")
query_str_agg = "SELECT venue, avg(price) FROM 'concerts.parquet' GROUP BY venue;"
t3 = time.time()
response = duckdb.sql(query_str_agg)
t4 = time.time()
print(response)
dt2 = t4-t3
print(f'Time taken: {dt2:2f}')
