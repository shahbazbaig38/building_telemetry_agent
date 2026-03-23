# Building Telemetry SQL Agent

A friendly, dynamic AI assistant for building telemetry analytics. Users can ask questions in natural language, and the agent generates safe read-only SQL automatically.

## ✅ Project Goals

- Build a natural-language to SQL agent for monitoring building telemetry
- Only allow `SELECT` queries to prevent data modification
- Use real telemetry data from `data/data.csv`
- Keep the experience interactive and prompt-aware
- Use `langchain_community` SQL agent utilities with `SQLDatabase` + `create_sql_agent`

## 📁 Repository Structure

- `data/` - source CSV and generated SQLite DB
  - `data.csv` - raw telemetry data
  - `telemetry_sqlite.db` - generated SQLite DB used by agent
- `src/` - application code
  - `create_sqlite_db.py` - converts `data.csv` to SQLite database
  - `agent.py` - core AI agent code (dynamic SQL generation)
- `pyproject.toml` - dependencies
- `README.md` - this file

## 🛠️ Setup & Installation

1. Create virtual environment and install deps:

```bash
# Use your preferred environment manager, e.g. python -m venv .venv
.venv\Scripts\activate
uv install
```

2. Build the SQLite dataset:

```bash
uv run src/create_sqlite_db.py
```

3. Run the agent:

```bash
uv run src/agent.py
```

## 🧠 How It Works

- `create_sqlite_db.py`:
  - Reads `data/data.csv` with Pandas
  - Creates `data/telemetry_sqlite.db` with a `telemetry` table

- `agent.py`:
  - Connects via `SQLDatabase.from_uri('sqlite:///data/telemetry_sqlite.db')`
  - Uses `create_sql_agent(...)` with `llm=ChatOllama(...)`
  - Agent prompt contains schema, read-only safety rules, and examples
  - User queries are transformed into SQL and executed, results returned

## 🔐 Safety & Restrictions

Agent is instructed:
- Only execute `SELECT` queries
- No `INSERT`, `UPDATE`, `DELETE`, `ALTER`, or `DROP`
- If user asks modification, it should refuse and suggest read-only alternatives

## 📊 Example Queries

- "What is the average indoor temperature for the past 24 hours?"
- "Show me peak electricity consumption by hour."
- "Compare indoor vs outdoor humidity trends."
- "Detect if CO2 has been above 900 ppm in last 3 hours."

## 🔍 Data Schema (telemetry table)

- `timestamp`: TEXT (ISO-like `YYYY-MM-DD HH:MM`)
- `electricity_consumption`: REAL
- `district_heating`: REAL
- `people_counter`: REAL
- `indoor_average_temperature`: REAL
- `indoor_average_humidity`: REAL
- `indoor_co2`: REAL
- `outside_temperature`: REAL
- `outside_humidity`: REAL
- `outside_pressure`: REAL
- `outside_wind_speed`: REAL
- `outside_wind_direction`: REAL
- `outside_precipitation`: REAL
- `outside_solar_radiation`: REAL
- `outside_cloud_cover`: REAL
- `snow_depth`: REAL

## 🧪 Validation

1. Confirm DB created:
```python
import sqlite3
conn = sqlite3.connect('data/telemetry_sqlite.db')
print(conn.execute('SELECT COUNT(*) FROM telemetry').fetchone())
```
2. Agent test query:
```python
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama

llm = ChatOllama(model='llama3.1:latest', temperature=0.1)
db = SQLDatabase.from_uri('sqlite:///data/telemetry_sqlite.db')
agent = create_sql_agent(llm=llm, db=db, agent_type='openai-tools', verbose=True)
print(agent.invoke('What is the average indoor temperature?')['output'])
```

## 🚀 Notes

- This repo is now cleaned from temporary scripts (`create_db.py`, `duck_db_creation.py`, `test_agent.py`, `test_db.py`)
- Agent is dynamic and more compliant with your goal: NLP-to-SQL with `langchain_community` toolkit
- Keep Ollama local inference running when using agent
</content>
<parameter name="filePath">c:\Users\sh24397\OneDrive - Savonia-ammattikorkeakoulu\Desktop\github_projects\building_telemetry_agent\README.md
