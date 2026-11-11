# Power BI, FP&A, Data Engineering and GenAI

[![CI](https://github.com/Shashidhara-KB/data-engineering-genai-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/Shashidhara-KB/data-engineering-genai-portfolio/actions/workflows/ci.yml)

This repository collects projects related to the work described in my résumé. Power BI and FP&A are my strongest areas. The data-engineering examples show how I prepare and validate reporting data with SQL, PySpark and Delta Lake. The GenAI folders are prototypes and are labelled accordingly.

All examples use synthetic or public data. They do not contain employer datasets, internal code, credentials or report designs.

## Power BI and FP&A

| Project | Main content | Status |
|---|---|---|
| [FP&A Performance Management](projects/fpa-power-bi-performance-management/) | SQL star schema, DAX, Power Query and dynamic RLS for Actual/Budget/Forecast reporting | Reference implementation |
| [FTE and Workforce Analytics](projects/fte-workforce-analytics/) | Monthly FTE model, validation rules, workforce KPIs and Power BI measures | Reference implementation |
| [Budget Data Integration](projects/budget-data-integration-automation/) | SharePoint-to-Azure SQL flow, staging/final procedures, unpivoting and DirectQuery output | Reference implementation |

## Data engineering

| Project | Main content | Status |
|---|---|---|
| [Finance Reporting Modernization](projects/finance-reporting-modernization/) | Runnable Bronze/Silver/Gold Spark pipeline, quarantine, reconciliation and reporting view | Working example |
| [Retail Sales Lakehouse](projects/retail-sales-lakehouse/) | PySpark transformations, Delta merge and automated tests | Working example |
| [Azure Olympics Lakehouse](https://github.com/Shashidhara-KB/Azure) | Public-data transformations, Gold metrics and tests | Working example |

## GenAI

| Project | Main content | Status |
|---|---|---|
| [FP&A Knowledge Assistant](projects/fpa-knowledge-assistant/) | Local retrieval, confidence threshold and a roadmap for cited RAG answers | Prototype |
| [KPI Help Service](projects/report-kpi-help-assistant/) | Controlled KPI catalogue lookup with source and ownership fields | Prototype |

## Status definitions

- **Working example:** runnable code with sample data and automated checks
- **Reference implementation:** documented design and reusable components, but not a complete deployed application
- **Prototype:** early implementation used to test an idea

## Repository layout

```text
projects/   Project code, sample data and documentation
tests/      Automated checks shared across projects
.github/    CI and dependency configuration
```

## Current priorities

1. Add synthetic Power BI report visuals and a PBIP/PBIX example.
2. Extend the knowledge assistant with embeddings, citations and retrieval evaluation.
3. Keep the finance data projects runnable locally without requiring an Azure subscription.
