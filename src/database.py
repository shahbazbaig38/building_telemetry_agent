import sqlite3
from .sql_safety import check_forbidden_sql


def execute_sql(query: str) -> str:
    if not check_forbidden_sql(query):
        return "Rejected: Query contains disallowed database modification operation. Only SELECTs are permitted."

    conn = sqlite3.connect("data/telemetry_sqlite.db")
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description] if cursor.description else []
        rows = cursor.fetchall()

        if not rows:
            return "Query executed successfully but returned no rows."

        out = ["\t".join(columns)]
        out += ["\t".join(map(str, row)) for row in rows[:50]]
        if len(rows) > 50:
            out.append(f"... and {len(rows) - 50} more rows")
        return "\n".join(out)
    except sqlite3.Error as e:
        msg = str(e)
        if "no such column" in msg.lower():
            return (
                f"SQL error: {msg}. "
                "Hint: make sure all string/text values are quoted (e.g. '2024-01-01') "
                "and that column names exactly match the telemetry schema."
            )
        return f"SQL error: {msg}"
    finally:
        conn.close()