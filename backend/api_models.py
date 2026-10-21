"""Optional typed models for v1 integrations; legacy payloads remain unchanged."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class RunRequest(BaseModel):
    sql: str = Field(min_length=1)


class CompareRequest(BaseModel):
    generated_sql: str = Field(min_length=1)
    target_table: str = Field(min_length=1)
    target_column: str = Field(min_length=1)


class BigQueryField(BaseModel):
    name: str
    type: str
    mode: str


class RunResponse(BaseModel):
    job_id: str
    project: str | None
    location: str | None
    row_count: int
    schema_: list[BigQueryField] = Field(alias="schema")
    rows: list[dict[str, Any]]
    bytes_processed: int | None
    elapsed_ms: float
    truncated: bool
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class CompareResponse(BaseModel):
    status: Literal["PASS", "FAIL"]
    target_table: str
    target_column: str
    generated_row_count: int
    target_row_count: int
    mismatch_value_count: int
    deviations: list[dict[str, Any]]
    elapsed_ms: float
    comparison_mode: str
    model_config = ConfigDict(extra="allow")
