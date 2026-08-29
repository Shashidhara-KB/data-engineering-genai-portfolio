import importlib.util
from pathlib import Path

from pyspark.sql import functions as F


MODULE_PATH = Path(__file__).parents[1] / "src" / "transformations.py"
SPEC = importlib.util.spec_from_file_location("transformations", MODULE_PATH)
transformations = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transformations)


def sample_bronze(spark):
    rows = [
        ("T1", "2026-08-01", "C1", "P1", 2, 10.0, "2026-08-01 10:00:00"),
        ("T1", "2026-08-01", "C1", "P1", 3, 10.0, "2026-08-01 11:00:00"),
        ("T2", "2026-08-01", "C2", "P2", -1, 5.0, "2026-08-01 12:00:00"),
    ]
    columns = [
        "transaction_id", "transaction_date", "customer_id", "product_id",
        "quantity", "unit_price", "updated_at",
    ]
    return transformations.enrich_bronze(
        spark.createDataFrame(rows, columns), "sales_20260801.csv"
    )


def test_silver_keeps_latest_valid_record(spark):
    result = transformations.build_silver(sample_bronze(spark)).collect()
    assert len(result) == 1
    assert result[0]["quantity"] == 3
    assert result[0]["sales_amount"] == 30.0


def test_quarantine_captures_failure_reason(spark):
    result = transformations.build_quarantine(sample_bronze(spark)).collect()
    assert len(result) == 1
    assert result[0]["quality_failure_reason"] == "non_positive_quantity"


def test_daily_sales_metrics(spark):
    silver = transformations.build_silver(sample_bronze(spark))
    result = transformations.build_daily_sales(silver).drop("refreshed_at").collect()[0]
    assert result["total_sales"] == 30.0
    assert result["order_count"] == 1
    assert result["units_sold"] == 3
    assert result["unique_customers"] == 1
