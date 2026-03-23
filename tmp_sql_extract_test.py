from src.sql_generation import _extract_select_from_response

tests = [
    "```sql\nSELECT timestamp, electricity_consumption\nFROM telemetry\nWHERE electricity_consumption > 50\n```\nReasoning",
    "SELECT timestamp, electricity_consumption FROM telemetry LIMIT 1\nDetails",
    "No sql",
]

for t in tests:
    try:
        print('====')
        print('IN:', t.replace('\n', ' | '))
        print('OUT:', _extract_select_from_response(t))
    except Exception as e:
        print('ERR:', e)
