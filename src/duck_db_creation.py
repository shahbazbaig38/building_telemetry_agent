import duckdb
import pandas as pd


data = duckdb.read_csv("data/data.csv")

duckdb.sql("CREATE TABLE telemetry AS SELECT * FROM data")

# save the database to a duckdb file in data/telemetry.duckdb
duckdb.sql("EXPORT DATABASE 'data/telemetry.duckdb'")
print(duckdb.sql("SELECT * FROM telemetry LIMIT 10"))