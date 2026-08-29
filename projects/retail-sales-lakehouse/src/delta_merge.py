"""Delta Lake incremental upsert helper."""

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession


def merge_transactions(
    spark: SparkSession,
    updates: DataFrame,
    target_table: str,
) -> None:
    """Insert new transactions and update only newer versions."""
    if not spark.catalog.tableExists(target_table):
        updates.write.format("delta").mode("overwrite").saveAsTable(target_table)
        return

    target = DeltaTable.forName(spark, target_table)
    (
        target.alias("target")
        .merge(
            updates.alias("source"),
            "target.transaction_id = source.transaction_id",
        )
        .whenMatchedUpdateAll(
            condition="source.updated_at >= target.updated_at"
        )
        .whenNotMatchedInsertAll()
        .execute()
    )
