# Power BI, FP&A, Data Engineering & GenAI Portfolio

[![CI](https://github.com/Shashidhara-KB/data-engineering-genai-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/Shashidhara-KB/data-engineering-genai-portfolio/actions/workflows/ci.yml)

My strongest experience is in Power BI and FP&A reporting. This portfolio starts with financial reporting models, DAX, Power Query and workforce analytics, then shows related Databricks/PySpark work and exploratory GenAI prototypes.

The code here is **portfolio work using synthetic or public data**, not internal employer code. A **working example** includes runnable code and tests; a **reference implementation** demonstrates a design pattern; and a **prototype** is still in development.

## Power BI & FP&A — primary focus

| Project | What it demonstrates | Status |
|---|---|---|
| [FP&A Performance Management](projects/fpa-power-bi-performance-management/) | SQL star schema, DAX measures, Power Query and dynamic RLS pattern for Actual/Budget/Forecast reporting | Reference implementation |
| [FTE & Workforce Analytics](projects/fte-workforce-analytics/) | Workforce transformations and example Power BI measures | Reference implementation |
| [Budget Data Integration](projects/budget-data-integration-automation/) | SQL staging/final pattern and a Logic Apps workflow outline for budget reporting | Reference implementation |

## Data Engineering — hands-on projects

| Project | What it demonstrates | Status |
|---|---|---|
| [Finance Reporting Modernization](projects/finance-reporting-modernization/) | Runnable Bronze/Silver/Gold Spark job, data-quality quarantine, reconciliation and reporting SQL view | Working example |
| [Retail Sales Lakehouse](projects/retail-sales-lakehouse/) | PySpark transformations, Delta merge and tests | Working example |
| [Azure Olympics Lakehouse](https://github.com/Shashidhara-KB/Azure) | Public data transformations, Gold metrics and tests | Working example |

## GenAI — learning and prototypes

| Project | What it demonstrates | Status |
|---|---|---|
| [FP&A Knowledge Assistant](projects/fpa-knowledge-assistant/) | Local document retrieval and a proposed RAG architecture for onboarding questions | Prototype |
| [KPI Help Service](projects/report-kpi-help-assistant/) | Searchable KPI catalogue with source and owner details | Prototype |

## Repository layout

```text
projects/   Project code, sample data and documentation
tests/      Cross-project automated tests
.github/    CI and dependency configuration
```

## What I am improving next

My priority is to add clearer Power BI model screenshots, documented DAX examples and report walkthroughs. For GenAI, I plan to extend the local retrieval prototype into a runnable RAG application with source citations and evaluation examples.

I aim to describe each project's current state accurately rather than claim unverified business outcomes.
