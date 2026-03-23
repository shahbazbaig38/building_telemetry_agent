import re

FORBIDDEN_SQL_PATTERNS = [
    r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b", r"\bALTER\b", r"\bDROP\b",
    r"\bTRUNCATE\b", r"\bREPLACE\b", r"\bCREATE\b", r"\bGRANT\b", r"\bREVOKE\b"
]


def check_forbidden_sql(query: str) -> bool:
    q = query.upper()
    for pat in FORBIDDEN_SQL_PATTERNS:
        if re.search(pat, q):
            return False
    return True