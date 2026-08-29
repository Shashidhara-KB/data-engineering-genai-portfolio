"""Synthetic workforce transformations with no personally identifiable data."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def build_monthly_workforce(df: DataFrame) -> DataFrame:
    latest = Window.partitionBy("employee_key", "period_end").orderBy(F.col("updated_at").desc())
    return (
        df.withColumn("period_end", F.to_date("period_end"))
        .withColumn("fte", F.col("fte").cast("decimal(8,3)"))
        .withColumn("base_pay", F.col("base_pay").cast("decimal(19,2)"))
        .withColumn("row_number", F.row_number().over(latest))
        .filter(F.col("row_number") == 1)
        .filter((F.col("fte") >= 0) & (F.col("fte") <= 1.5))
        .drop("row_number")
    )


def build_gold_summary(df: DataFrame) -> DataFrame:
    return df.groupBy("period_end", "region", "entity", "function_name").agg(
        F.countDistinct("employee_key").alias("headcount"),
        F.sum("fte").alias("fte"),
        F.sum("base_pay").alias("base_pay"),
    ).withColumn("base_pay_per_fte", F.round(F.col("base_pay") / F.col("fte"), 2))
