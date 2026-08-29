"""Reusable transformations for the Retail Sales Lakehouse project."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


REQUIRED_COLUMNS = {
    "transaction_id",
    "transaction_date",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
    "updated_at",
}


def validate_schema(df: DataFrame) -> None:
    """Fail early when required source fields are unavailable."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def enrich_bronze(df: DataFrame, source_file: str) -> DataFrame:
    """Add operational metadata while preserving source-aligned records."""
    validate_schema(df)
    return (
        df.withColumn("ingested_at", F.current_timestamp())
        .withColumn("source_file", F.lit(source_file))
        .withColumn("transaction_date", F.to_date("transaction_date"))
        .withColumn("updated_at", F.to_timestamp("updated_at"))
    )


def apply_quality_rules(df: DataFrame) -> DataFrame:
    """Annotate each record with a deterministic validation result."""
    failure_reason = (
        F.when(F.col("transaction_id").isNull(), F.lit("missing_transaction_id"))
        .when(F.col("product_id").isNull(), F.lit("missing_product_id"))
        .when(F.col("transaction_date").isNull(), F.lit("invalid_transaction_date"))
        .when(F.col("quantity") <= 0, F.lit("non_positive_quantity"))
        .when(F.col("unit_price") < 0, F.lit("negative_unit_price"))
    )
    return (
        df.withColumn("quality_failure_reason", failure_reason)
        .withColumn("is_valid", F.col("quality_failure_reason").isNull())
    )


def build_silver(df: DataFrame) -> DataFrame:
    """Keep valid rows, retain the latest update, and calculate revenue."""
    checked = apply_quality_rules(df).filter(F.col("is_valid"))
    latest = Window.partitionBy("transaction_id").orderBy(
        F.col("updated_at").desc_nulls_last(), F.col("ingested_at").desc()
    )
    return (
        checked.withColumn("row_number", F.row_number().over(latest))
        .filter(F.col("row_number") == 1)
        .drop("row_number", "is_valid", "quality_failure_reason")
        .withColumn(
            "sales_amount",
            F.round(F.col("quantity") * F.col("unit_price"), 2),
        )
    )


def build_quarantine(df: DataFrame) -> DataFrame:
    """Return invalid records with an actionable failure reason."""
    return apply_quality_rules(df).filter(~F.col("is_valid")).drop("is_valid")


def build_daily_sales(df: DataFrame) -> DataFrame:
    """Produce reporting-ready daily commercial KPIs."""
    return (
        df.groupBy("transaction_date")
        .agg(
            F.round(F.sum("sales_amount"), 2).alias("total_sales"),
            F.countDistinct("transaction_id").alias("order_count"),
            F.sum("quantity").alias("units_sold"),
            F.countDistinct("customer_id").alias("unique_customers"),
        )
        .withColumn("refreshed_at", F.current_timestamp())
    )


def build_product_performance(df: DataFrame) -> DataFrame:
    """Produce product-level KPIs for merchandising analysis."""
    return df.groupBy("transaction_date", "product_id").agg(
        F.round(F.sum("sales_amount"), 2).alias("product_sales"),
        F.sum("quantity").alias("units_sold"),
        F.countDistinct("transaction_id").alias("order_count"),
    )
