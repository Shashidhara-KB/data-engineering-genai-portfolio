# Data Engineering & GenAI Portfolio

[![CI](https://github.com/Shashidhara-KB/data-engineering-genai-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/Shashidhara-KB/data-engineering-genai-portfolio/actions/workflows/ci.yml)

This repository contains projects I use to practise and demonstrate data engineering, Power BI and GenAI concepts. Most examples are based on the kind of finance and reporting problems I know well, but all data and business names are synthetic or public.

I have kept the projects at different levels of completion. A **working example** has runnable code and tests; a **reference implementation** demonstrates a useful pattern; and a **prototype** is an early implementation that I am still developing.

## Projects

| Project | What is included | Status |
|---|---|---|
| [Finance Reporting Modernization](projects/finance-reporting-modernization/) | Runnable Bronze/Silver/Gold Spark job, quarantine, reconciliation, synthetic finance data and Power BI SQL view | Working example |
| [Retail Sales Lakehouse](projects/retail-sales-lakehouse/) | PySpark transformations, data-quality quarantine, Delta merge and unit tests | Working example |
| [Azure Olympics Lakehouse](https://github.com/Shashidhara-KB/Azure) | Public datasets, PySpark transformations, Gold metrics and tests | Working example |
| [FP&A Performance Management](projects/fpa-power-bi-performance-management/) | SQL star schema, DAX, Power Query and an RLS pattern | Reference implementation |
| [FTE & Workforce Analytics](projects/fte-workforce-analytics/) | Workforce transformations and example DAX measures | Reference implementation |
| [Budget Data Integration](projects/budget-data-integration-automation/) | SQL staging/final pattern and a Logic Apps workflow outline | Reference implementation |
| [FP&A Knowledge Assistant](projects/fpa-knowledge-assistant/) | A small local retriever plus the planned RAG architecture | Prototype |
| [KPI Help Service](projects/report-kpi-help-assistant/) | A searchable KPI catalogue with source and owner details | Prototype |

## Repository layout

```text
projects/   Project code, sample data and documentation
tests/      Cross-project automated tests
.github/    CI and dependency configuration
```

## Current priorities

I add code here only when I can explain the design choices and trade-offs. My next priorities are to add visual proof for the Power BI project and turn the knowledge-assistant prototype into a runnable RAG application.
