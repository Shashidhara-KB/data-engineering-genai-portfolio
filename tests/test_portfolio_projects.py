import importlib.util
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_finance_pipeline_keeps_latest_record_and_reconciles(spark):
    module = load_module(
        "finance_medallion",
        "projects/finance-reporting-modernization/src/finance_medallion.py",
    )
    rows = [
        ("1", "2026-01-31", "E01", "A100", "CC10", "ACT", "EUR", "90", datetime(2026, 2, 1)),
        ("1", "2026-01-31", "E01", "A100", "CC10", "ACT", "EUR", "100", datetime(2026, 2, 2)),
        ("2", "2026-01-31", "E01", "A200", "CC10", "ACT", "EUR", "50", datetime(2026, 2, 1)),
    ]
    columns = [
        "record_id", "posting_date", "entity", "account", "cost_center",
        "scenario", "currency", "amount", "updated_at",
    ]

    silver = module.build_silver(spark.createDataFrame(rows, columns))
    assert silver.count() == 2

    control = module.reconciliation(silver).first()
    assert control.row_count == 2
    assert control.control_total == Decimal("150.00")

    gold = module.build_gold_pnl(silver).collect()
    assert sum(row.record_count for row in gold) == 2


def test_finance_pipeline_rejects_missing_columns(spark):
    module = load_module(
        "finance_validation",
        "projects/finance-reporting-modernization/src/finance_medallion.py",
    )
    with pytest.raises(ValueError, match="Missing required columns"):
        module.validate_source(spark.createDataFrame([("1",)], ["record_id"]))


def test_workforce_pipeline_filters_invalid_fte_and_uses_latest_row(spark):
    module = load_module(
        "workforce_model",
        "projects/fte-workforce-analytics/src/workforce_model.py",
    )
    rows = [
        ("E1", "2026-01-31", "Europe", "NL01", "Finance", "0.8", "8000", datetime(2026, 2, 1)),
        ("E1", "2026-01-31", "Europe", "NL01", "Finance", "1.0", "10000", datetime(2026, 2, 2)),
        ("E2", "2026-01-31", "Europe", "NL01", "Finance", "2.0", "12000", datetime(2026, 2, 1)),
    ]
    columns = [
        "employee_key", "period_end", "region", "entity", "function_name",
        "fte", "base_pay", "updated_at",
    ]

    monthly = module.build_monthly_workforce(spark.createDataFrame(rows, columns))
    assert monthly.count() == 1

    summary = module.build_gold_summary(monthly).first()
    assert summary.headcount == 1
    assert summary.fte == Decimal("1.000")
    assert summary.base_pay_per_fte == Decimal("10000.00")


def test_retriever_ranks_relevant_evidence_and_handles_no_match():
    module = load_module(
        "retrieval",
        "projects/fpa-knowledge-assistant/src/retrieval.py",
    )
    chunks = [
        module.DocumentChunk("c1", "forecast.md", "Forecast submissions close on working day five."),
        module.DocumentChunk("c2", "access.md", "Report access is approved by the regional controller."),
    ]

    results = module.retrieve("When do forecast submissions close?", chunks, top_k=1)
    assert results[0][0].chunk_id == "c1"
    assert "[c1]" in module.build_grounded_context(results)
    assert module.build_grounded_context([], minimum_score=0.1) == "NO_RELEVANT_EVIDENCE"


def test_kpi_catalog_lookup_and_unknown_response():
    module = load_module(
        "kpi_service",
        "projects/report-kpi-help-assistant/src/kpi_service.py",
    )
    catalog = module.load_catalog(
        ROOT / "projects/report-kpi-help-assistant/data/kpi_catalog.json"
    )

    result = module.find_kpi("How is Net Sales calculated?", catalog)
    answer = module.format_answer(result)
    assert "Formula:" in answer
    assert "Commercial Finance" in answer
    assert "could not find" in module.format_answer(None).lower()


def test_budget_assets_have_expected_controls():
    workflow_path = (
        ROOT
        / "projects/budget-data-integration-automation/logic-app/workflow-outline.json"
    )
    sql_path = (
        ROOT
        / "projects/budget-data-integration-automation/sql/budget_pipeline.sql"
    )

    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    sql = sql_path.read_text(encoding="utf-8").upper()

    assert workflow["security"]["secrets_in_definition"] is False
    assert "WRITE SUCCESS OR FAILURE AUDIT RECORD" in {
        action.upper() for action in workflow["actions"]
    }
    for expected in ["SET XACT_ABORT ON", "BEGIN TRANSACTION", "THROW 50001", "CROSS APPLY"]:
        assert expected in sql
