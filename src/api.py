from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .sql_generation import generate_sql_from_nl, summarize_sql_result
from .database import execute_sql

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/api/query")
def query_sql(req: QueryRequest):
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query text is required")

    try:
        sql = generate_sql_from_nl(q)
        result = execute_sql(sql)
        explanation = summarize_sql_result(q, sql, result)
        return {
            "sql": sql,
            "result": result,
            "explanation": explanation,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
