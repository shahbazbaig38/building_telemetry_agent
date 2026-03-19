COPY telemetry FROM 'data/telemetry.duckdb/telemetry.csv' (FORMAT 'csv', header 1, delimiter ',', quote '"');
