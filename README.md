# Building Telemetry SQL Agent

A production-grade AI assistant for building telemetry analytics with natural language explanations. Users ask questions about building sensor data in plain English, and the agent generates safe read-only SQL automatically, executes it, and explains results in natural language.

## ✅ Project Goals

- Build a modular, natural-language-to-SQL agent for analyzing building telemetry
- Only allow `SELECT` queries to prevent data modification
- Use real sensor data from `data/data.csv` with a knowledge graph of sensor relationships
- Provide interactive CLI + web API + minimal frontend for multiple interfaces
- Generate SQL robustly (handle markdown fences, multi-line queries)
- Explain query results in natural language for non-technical users

## 📁 Repository Structure

- `data/` - source CSV and generated SQLite DB
  - `data.csv` - raw telemetry data
  - `telemetry_sqlite.db` - SQLite database used by agent
- `src/` - modular application code
  - `__init__.py` - package initialization
  - `agent.py` - interactive CLI interface
  - `api.py` - FastAPI web service
  - `sql_generation.py` - LLM + SQL generation + natural language summarization
  - `database.py` - SQL execution layer with safety checks
  - `sql_safety.py` - forbidden SQL pattern detection
  - `knowledge_graph.py` - sensor relationship knowledge base
  - `create_sqlite_db.py` - converts `data.csv` to SQLite database
- `web/` - frontend
  - `index.html` - minimal web UI for API interaction
- `pyproject.toml` - project metadata and dependencies
- `README.md` - this file

## 🛠️ Setup & Installation

1. Ensure Ollama is running locally:
```bash
ollama serve
```

2. Create virtual environment and install dependencies:

3. Create the SQLite database:
```bash
python src/create_sqlite_db.py
```

## 🚀 Usage

### CLI Interface

Run the interactive agent:
```bash
python -m src.agent
```

Example interaction:
```
You: Show me average electricity consumption in the last 24 hours
--> Generated SQL: SELECT AVG(electricity_consumption) FROM telemetry WHERE timestamp > datetime('now', '-1 day')
--> Result:
AVG(electricity_consumption)
45.2

--> Interpretation:
The average electricity consumption over the past 24 hours is 45.2 units. This indicates typical HVAC and building system usage patterns. No unusual spikes detected.
```

### Web API

Start the FastAPI server:
```bash
uvicorn src.api:app --reload
```

API endpoint: `POST /api/query`

Request:
```json
{
  "query": "What is the average indoor temperature?"
}
```

Response:
```json
{
  "sql": "SELECT AVG(indoor_average_temperature) FROM telemetry",
  "result": "AVG(indoor_average_temperature)\n22.5",
  "explanation": "The average indoor temperature across all readings is 22.5°C, which is within a comfortable range and indicates proper HVAC control."
}
```

### Web UI

After starting FastAPI, open `web/index.html` in a browser (or serve via HTTP):
```bash
python -m http.server 8080 --directory web
```

Access at `http://localhost:8080` and interact with the assistant through the UI.

## 🧠 How It Works

### Core Components

1. **`sql_generation.py`** - LLM-driven SQL generation
   - `get_telemetry_columns()` - dynamically loads actual database schema
   - `generate_sql_from_nl(user_question)` - LLM transforms natural language to SQL
   - `_extract_select_from_response()` - robust extraction handles markdown fences and multi-line queries
   - `summarize_sql_result(user_question, sql, result)` - LLM explains results in plain English
   - `SYSTEM_PROMPT` - comprehensive rules + knowledge graph context

2. **`database.py`** - Safe SQL execution
   - `execute_sql(query)` - runs SELECT queries safely
   - Checks against forbidden SQL patterns (INSERT, UPDATE, DELETE, etc.)
   - Provides helpful error hints for common issues (e.g., "no such column" with quoting guidance)

3. **`sql_safety.py`** - SQL validation
   - `check_forbidden_sql()` - regex-based forbidden keyword detection

4. **`knowledge_graph.py`** - Sensor relationship context
   - `SENSOR_KB` - dict mapping sensor names to related sensors and their effects
   - `generate_kb_hint()` - formats graph for LLM prompt

5. **`agent.py`** - CLI interface
   - Interactive loop asking user questions
   - Chains `generate_sql_from_nl` → `execute_sql` → `summarize_sql_result`
   - Prints SQL, results, and interpretation

6. **`api.py`** - REST API interface
   - FastAPI app with `/api/query` endpoint
   - CORS enabled for web UI
   - Returns JSON with `sql`, `result`, and `explanation`

7. **`web/index.html`** - Minimal web frontend
   - Input field for natural language queries
   - Displays SQL, result rows, and explanation
   - Clears previous query outputs when running new query

## 🔐 Safety & Restrictions

Multiple layers of defense:
1. **System Prompt Rules** - LLM instructed to only generate `SELECT` statements
2. **Regex Validation** - `sql_safety.check_forbidden_sql()` blocks INSERT/UPDATE/DELETE/ALTER/DROP/TRUNCATE/GRANT/REVOKE
3. **Error Handling** - Database layer catches and explains SQL errors with hints
4. **Schema Validation** - Prompt dynamically includes actual database columns, reducing hallucination

## 📊 Data Schema (telemetry table)

All columns are auto-loaded dynamically from database. Example columns:
- `timestamp` TEXT
- `electricity_consumption` REAL
- `district_heating` REAL
- `people_counter` REAL
- `indoor_average_temperature` REAL
- `indoor_average_humidity` REAL
- `indoor_co2` REAL
- `outside_temperature` REAL
- `outside_humidity` REAL
- `outside_pressure` REAL
- `outside_wind_speed` REAL
- `outside_wind_direction` REAL
- `outside_precipitation` REAL
- `outside_solar_radiation` REAL
- `outside_cloud_cover` REAL
- `snow_depth` REAL

## 💡 Key Features

- **Modular Architecture**: Each concern (SQL generation, database, safety, UI) is separated
- **Robust SQL Parsing**: Handles markdown fences (```sql), multi-line queries, edge cases
- **Natural Language Output**: Uses LLM to explain query results in plain English for non-technical users
- **Dynamic Schema**: Loads actual database columns on startup, preventing column name mismatches
- **Error Hints**: Provides contextual guidance when queries fail (e.g., missing quotes recommendation)
- **Multiple Interfaces**: CLI, REST API, and web UI all available
- **Production Safety**: Read-only enforcement via regex + prompt rules + error handling

## 🧪 Testing & Validation

1. Verify database:
```bash
sqlite3 data/telemetry_sqlite.db "SELECT COUNT(*) FROM telemetry;"
```

2. Test agent directly:
```bash
python -m src.agent
# Type: Show first 5 rows
```

3. Test API:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Average indoor temperature"}'
```

4. Test web UI:
   - Open `web/index.html` in browser after starting API
   - Enter a query and verify SQL, result, and explanation appear

## 🚀 Notes

- **Ollama LLM**: Uses `llama3.1:latest` by default; ensure Ollama is running locally
- **SQLite Database**: Auto-created from CSV on `create_sqlite_db.py` execution
- **Temperature**: Prompt uses `temperature=0.1` for consistent, deterministic SQL generation
- **CORS Enabled**: API allows requests from any origin (suitable for local testing)

</content>
<parameter name="filePath">c:\Users\sh24397\OneDrive - Savonia-ammattikorkeakoulu\Desktop\github_projects\building_telemetry_agent\README.md
