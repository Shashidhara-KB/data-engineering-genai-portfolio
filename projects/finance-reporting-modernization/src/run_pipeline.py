"""Command-line entry point for the finance reporting pipeline."""

import argparse
from pathlib import Path

from pyspark.sql import SparkSession

from finance_medallion import (
    build_gold_cost_center,
    build_gold_pnl,
    reconciliation,
    split_silver_and_quarantine,
)


def write_table(df, output: Path, name: str, file_format: str) -> None:
    df.write.mode("overwrite").format(file_format).save(str(output / name))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build finance Silver and Gold datasets")
    parser.add_argument("--input", required=True, help="Input CSV file or directory")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--format", choices=("parquet", "delta"), default="parquet")
    args = parser.parse_args()

    spark = SparkSession.builder.appName("finance-reporting-modernization").getOrCreate()
    raw = spark.read.option("header", True).csv(args.input)

    output = Path(args.output)
    valid, quarantine = split_silver_and_quarantine(raw)
    write_table(raw, output, "bronze/finance_transactions", args.format)
    write_table(valid, output, "silver/finance_transactions", args.format)
    write_table(quarantine, output, "quarantine/finance_transactions", args.format)
    write_table(build_gold_pnl(valid), output, "gold/pnl_summary", args.format)
    write_table(
        build_gold_cost_center(valid),
        output,
        "gold/cost_center_summary",
        args.format,
    )
    write_table(reconciliation(valid), output, "controls/reconciliation", args.format)

    print(
        f"Pipeline complete: valid={valid.count()}, "
        f"quarantined={quarantine.count()}, format={args.format}"
    )
    spark.stop()


if __name__ == "__main__":
    main()
