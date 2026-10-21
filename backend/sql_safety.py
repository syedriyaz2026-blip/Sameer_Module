"""Conservative read-only SQL checks used before BigQuery execution."""
from __future__ import annotations

import re

from api_errors import TransformSQLError

_MUTATING = re.compile(r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|CREATE|ALTER|TRUNCATE|CALL|EXPORT)\b", re.I)


def assert_read_only(sql: str) -> None:
    text = str(sql or "").strip()
    if not text:
        raise TransformSQLError("INVALID_REQUEST", "sql is required", 400)
    without_comments = re.sub(r"--[^\n]*|/\*.*?\*/", " ", text, flags=re.S)
    statements = [part.strip() for part in without_comments.split(";") if part.strip()]
    if len(statements) != 1:
        raise TransformSQLError("SQL_NOT_SELECT", "Only one read-only SELECT statement is allowed", 400)
    if not re.match(r"^(SELECT|WITH)\b", statements[0], re.I):
        raise TransformSQLError("SQL_NOT_SELECT", "Only SELECT or WITH queries are allowed", 400)
    match = _MUTATING.search(statements[0])
    if match:
        raise TransformSQLError("SQL_NOT_SELECT", f"Statement contains prohibited keyword: {match.group(1).upper()}", 400)
