"""Governed KPI catalogue service for a conversational help assistant."""

import json
from pathlib import Path


def load_catalog(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        records = json.load(handle)
    required = {"kpi_id", "name", "definition", "formula", "report_page", "owner", "source"}
    for record in records:
        missing = required.difference(record)
        if missing:
            raise ValueError(f"KPI {record.get('kpi_id', '<unknown>')} is missing {sorted(missing)}")
    return records


def find_kpi(question: str, catalog: list[dict]) -> dict | None:
    normalized = question.lower()
    for kpi in catalog:
        if kpi["name"].lower() in normalized or kpi["kpi_id"].replace("_", " ") in normalized:
            return kpi
    return None


def format_answer(kpi: dict | None) -> str:
    if not kpi:
        return "I could not find an approved KPI definition. Please contact the report owner."
    return (
        f"{kpi['name']}: {kpi['definition']}\n"
        f"Formula: {kpi['formula']}\nReport page: {kpi['report_page']}\n"
        f"Owner: {kpi['owner']}\nSource: {kpi['source']}"
    )
