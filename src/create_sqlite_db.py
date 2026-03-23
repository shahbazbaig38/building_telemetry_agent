import pandas as pd
import sqlite3

# Load CSV data
df = pd.read_csv('data/data.csv')

# Create SQLite database
conn = sqlite3.connect('data/telemetry_sqlite.db')

# Write to SQLite
df.to_sql('telemetry', conn, if_exists='replace', index=False)

# Verify
print("Database created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

conn.close()