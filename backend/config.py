"""Validated runtime configuration for the TransformSQL service."""
from __future__ import annotations

import os
from dataclasses import dataclass


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int, minimum: int = 0) -> int:
    try:
        return max(minimum, int(os.getenv(name, str(default))))
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


@dataclass(frozen=True)
class Settings:
    env: str
    project: str | None
    location: str | None
    max_rows: int
    max_bytes_billed: int | None
    dry_run_enabled: bool
    cost_display_enabled: bool
    pii_masking_enabled: bool
    vertex_suggestions_enabled: bool
    audit_log_enabled: bool
    demo_login_enabled: bool
    read_only_sql_enabled: bool
    cors_allowed_origins: tuple[str, ...]


def load_settings() -> Settings:
    env = os.getenv("ENV", "local").strip().lower()
    demo = _bool("DEMO_LOGIN_ENABLED", env == "local")
    if env != "local":
        demo = False
    raw_max_bytes = os.getenv("BIGQUERY_MAX_BYTES_BILLED", "").strip()
    max_bytes = int(raw_max_bytes) if raw_max_bytes else None
    origins = tuple(x.strip() for x in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080").split(",") if x.strip())
    return Settings(
        env=env,
        project=os.getenv("BIGQUERY_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("BIGQUERY_LOCATION") or None,
        max_rows=min(_int("BIGQUERY_MAX_ROWS", 500, 1), 5000),
        max_bytes_billed=max_bytes,
        dry_run_enabled=_bool("TRANSFORMSQL_DRY_RUN_ENABLED", True),
        cost_display_enabled=_bool("TRANSFORMSQL_COST_DISPLAY_ENABLED", True),
        pii_masking_enabled=_bool("TRANSFORMSQL_PII_MASKING_ENABLED", env != "local"),
        vertex_suggestions_enabled=_bool("TRANSFORMSQL_VERTEX_SUGGESTIONS_ENABLED", False),
        audit_log_enabled=_bool("TRANSFORMSQL_AUDIT_LOG_ENABLED", True),
        demo_login_enabled=demo,
        read_only_sql_enabled=_bool("READ_ONLY_SQL_ENABLED", True),
        cors_allowed_origins=origins,
    )
