import sqlite3
from langchain_ollama import ChatOllama
from .knowledge_graph import generate_kb_hint

# ---------- LLM + SQL generation ----------
llm = ChatOllama(model="llama3.1:latest", temperature=0.1)


def get_telemetry_columns() -> str:
    conn = sqlite3.connect("data/telemetry_sqlite.db")
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(telemetry)")
        rows = cursor.fetchall()
        if not rows:
            return "(no telemetry table found)"
        lines = [f"- {row[1]} {row[2]}" for row in rows]
        return "\n".join(lines)
    except sqlite3.Error:
        return "(unable to load telemetry schema)"
    finally:
        conn.close()


SYSTEM_PROMPT = f"""
You are a production-grade building telemetry AI assistant connected to a SQLite database table `telemetry`.

Columns:
{get_telemetry_columns()}

{generate_kb_hint()}

Rules:
- MUST only generate a single SQL SELECT statement per query.
- MUST not include more than 10 rows in the output; use LIMIT to enforce this.
- MUST NOT generate INSERT/UPDATE/DELETE/ALTER/DROP/TRUNCATE/CREATE/GRANT/REVOKE.
- Must use valid column names exactly as defined; no misspelled or missing columns.
- Must quote string/date literals using single quotes (for example: `WHERE timestamp = '2024-01-01 00:00:00'`).
- Output format MUST be exactly:
  1. A code block containing only SQL on the first code block (language tag optional; prefer `sql`).
  2. A plain-text reasoning + summary section after the code block.
- Example correct response:
````
```sql
SELECT timestamp, electricity_consumption
FROM telemetry
WHERE electricity_consumption > 50
ORDER BY timestamp ASC
LIMIT 5;
```
The query returns the first 5 timestamps with consumption above 50.
````
- If query intent is not read-only data analysis, respond with a refusal message.
"""


def _extract_select_from_response(text: str) -> str:
    # Prefer SQL code block content to preserve full multi-line query
    code_lines = []
    in_code = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line.rstrip())

    if code_lines:
        sql_candidate = '\n'.join(code_lines).strip()
    else:
        # No code block: find first SELECT and collect subsequent lines that look SQL-like
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        start = None
        for i, line in enumerate(lines):
            if line.upper().startswith('SELECT'):
                start = i
                break
        if start is None:
            raise ValueError(f"LLM did not return a SELECT statement; got: {lines[0] if lines else '<empty>'}")

        sql_lines = []
        sql_markers = {'SELECT', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'LIMIT', 'JOIN', 'ON', 'HAVING', 'AND', 'OR', 'AS'}
        for line in lines[start:]:
            if not line:
                continue
            # If line looks like natural language and not query, stop.
            if not any(tok in line.upper().split() for tok in sql_markers) and ';' not in line and len(line.split()) < 2:
                break
            sql_lines.append(line)

        sql_candidate = ' '.join(sql_lines).strip()

    if not sql_candidate:
        raise ValueError("LLM did not return a SELECT statement; extracted SQL is empty")

    # Strip the final semicolon if present
    sql_candidate = sql_candidate.rstrip(';').strip()

    if not sql_candidate.upper().startswith('SELECT'):
        raise ValueError(f"LLM did not return a SELECT statement; got: {sql_candidate}")

    return sql_candidate


def generate_sql_from_nl(user_question: str) -> str:
    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"User question: {user_question}\nGenerate only one SELECT statement in a single sql code block, then summary."}
    ])

    text = response.content.strip()
    sql = _extract_select_from_response(text)

    if not sql.upper().startswith("SELECT"):
        raise ValueError(f"LLM did not return a SELECT statement; got: {sql}")

    return sql


def summarize_sql_result(user_question: str, sql: str, result: str) -> str:
    summary_prompt = f"""
You are an AI assistant that explains the result of a SQL query executed on the telemetry table.

User question: {user_question}
Generated SQL:
{sql}

Query output:
{result}

Write a concise natural language explanation of what this query does and what the result shows. Maintain clear language for non-technical users, include one short takeaway.
"""

    summary_response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": summary_prompt},
    ])

    return summary_response.content.strip()