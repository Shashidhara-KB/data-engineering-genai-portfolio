"""Transform synthetic finance extracts into Silver, quarantine and Gold datasets."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


REQUIRED = {
    "record_id", "posting_date", "entity", "account", "cost_center",
    "scenario", "currency", "amount", "updated_at",
}
ALLOWED_SCENARIOS = ("ACT", "BUD", "FCST")


def validate_source(df: DataFrame) -> None:
    missing = REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def standardize_source(df: DataFrame) -> DataFrame:
    """Apply types and standard naming before business validation."""
    validate_source(df)
    return (
        df.withColumn("posting_date", F.to_date("posting_date"))
        .withColumn("updated_at", F.to_timestamp("updated_at"))
        .withColumn("amount", F.col("amount").cast("decimal(19,2)"))
        .withColumn("entity", F.upper(F.trim("entity")))
        .withColumn("account", F.upper(F.trim("account")))
        .withColumn("cost_center", F.upper(F.trim("cost_center")))
        .withColumn("scenario", F.upper(F.trim("scenario")))
        .withColumn("currency", F.upper(F.trim("currency")))
    )


def add_quality_status(df: DataFrame) -> DataFrame:
    """Assign one rejection reason so failed rows remain explainable."""
    return df.withColumn(
        "quality_error",
        F.when(F.col("posting_date").isNull(), F.lit("invalid_posting_date"))
        .when(F.col("entity").isNull() | (F.col("entity") == ""), F.lit("missing_entity"))
        .when(F.col("account").isNull() | (F.col("account") == ""), F.lit("missing_account"))
        .when(F.col("amount").isNull(), F.lit("invalid_amount"))
        .when(~F.col("scenario").isin(*ALLOWED_SCENARIOS), F.lit("invalid_scenario"))
        .when(~F.col("currency").rlike("^[A-Z]{3}$"), F.lit("invalid_currency")),
    )


def split_silver_and_quarantine(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    """Keep the latest source version, then separate valid and rejected rows."""
    standardized = standardize_source(df)
    latest = Window.partitionBy("record_id").orderBy(F.col("updated_at").desc_nulls_last())
    checked = (
        standardized.withColumn("_row_number", F.row_number().over(latest))
        .filter(F.col("_row_number") == 1)
        .drop("_row_number")
        .transform(add_quality_status)
    )
    valid = checked.filter(F.col("quality_error").isNull()).drop("quality_error")
    quarantine = checked.filter(F.col("quality_error").isNotNull())
    return valid, quarantine


def build_silver(df: DataFrame) -> DataFrame:
    """Backward-compatible helper used by existing examples and tests."""
    valid, _ = split_silver_and_quarantine(df)
    return valid


def build_gold_pnl(df: DataFrame) -> DataFrame:
    return df.groupBy(
        F.year("posting_date").alias("fiscal_year"),
        F.month("posting_date").alias("fiscal_month"),
        "entity", "account", "scenario", "currency",
    ).agg(
        F.sum("amount").alias("amount"),
        F.count("record_id").alias("record_count"),
    )


def build_gold_cost_center(df: DataFrame) -> DataFrame:
    return df.groupBy(
        F.year("posting_date").alias("fiscal_year"),
        F.month("posting_date").alias("fiscal_month"),
        "entity", "cost_center", "scenario", "currency",
    ).agg(
        F.sum("amount").alias("amount"),
        F.count("record_id").alias("record_count"),
    )


def reconciliation(df: DataFrame) -> DataFrame:
    return df.groupBy("scenario", "currency").agg(
        F.count("record_id").alias("row_count"),
        F.sum("amount").alias("control_total"),
        F.max("updated_at").alias("latest_update"),
    )
