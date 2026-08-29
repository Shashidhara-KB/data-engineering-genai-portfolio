"""Synthetic finance Medallion transformations for portfolio demonstration."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


REQUIRED = {
    "record_id", "posting_date", "entity", "account", "cost_center",
    "scenario", "currency", "amount", "updated_at",
}


def validate_source(df: DataFrame) -> None:
    missing = REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def build_silver(df: DataFrame) -> DataFrame:
    validate_source(df)
    latest = Window.partitionBy("record_id").orderBy(F.col("updated_at").desc())
    return (
        df.withColumn("posting_date", F.to_date("posting_date"))
        .withColumn("amount", F.col("amount").cast("decimal(19,2)"))
        .withColumn("row_number", F.row_number().over(latest))
        .filter(F.col("row_number") == 1)
        .filter(F.col("entity").isNotNull() & F.col("account").isNotNull())
        .drop("row_number")
    )


def build_gold_pnl(df: DataFrame) -> DataFrame:
    return df.groupBy(
        F.year("posting_date").alias("fiscal_year"),
        F.month("posting_date").alias("fiscal_month"),
        "entity", "account", "scenario", "currency",
    ).agg(F.sum("amount").alias("amount"), F.count("record_id").alias("record_count"))


def reconciliation(df: DataFrame) -> DataFrame:
    return df.groupBy("scenario", "currency").agg(
        F.count("record_id").alias("row_count"),
        F.sum("amount").alias("control_total"),
        F.max("updated_at").alias("latest_update"),
    )
