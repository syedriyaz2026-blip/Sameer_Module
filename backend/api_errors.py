"""Stable API errors and correlation IDs."""
from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class TransformSQLError(Exception):
    code: str
    message: str
    status: int = 400
    details: dict | None = None
    retryable: bool = False

    def __str__(self) -> str:
        return self.message


def correlation_id() -> str:
    return uuid.uuid4().hex[:16]


def error_payload(error: Exception, request_id: str | None = None) -> dict:
    if isinstance(error, TransformSQLError):
        code, message, details, retryable = error.code, error.message, error.details or {}, error.retryable
    else:
        code, message, details, retryable = "INTERNAL_ERROR", str(error), {}, False
    return {"error": {"code": code, "message": message, "correlation_id": request_id or correlation_id(), "details": {**details, "retryable": retryable}}}
