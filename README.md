# Data Engineering & GenAI Portfolio

Production-minded portfolio projects demonstrating Azure data engineering, lakehouse architecture, analytics engineering, and Generative AI.

## About Me

I am a data and analytics professional with 12+ years of experience delivering enterprise reporting and data solutions. My current focus is building scalable data platforms and AI-enabled applications using Python, SQL, PySpark, Azure Databricks, Delta Lake, Power BI, Azure OpenAI, and RAG.

## Projects

| Project | Business problem | Core technologies | Status |
|---|---|---|---|
| [Retail Sales Lakehouse](projects/retail-sales-lakehouse/) | Build a reliable, incremental analytics pipeline from raw transactions to business-ready KPIs | PySpark, Delta Lake, Medallion Architecture, data quality, pytest, GitHub Actions | Complete |
| [FP&A Performance Management in Power BI](projects/fpa-power-bi-performance-management/) | Standardize Actual, Budget, Forecast, YTD, YTG, and full-year variance reporting | Power BI, DAX, Power Query, SQL, star schema, RLS | Complete |
| [Azure Olympics Lakehouse](https://github.com/Shashidhara-KB/Azure) | Transform multi-file Olympics data into country, medal-efficiency, and gender-participation metrics | Azure Databricks, PySpark, Delta Lake, data quality, pytest, GitHub Actions | Complete |
| [Finance Reporting Modernization](projects/finance-reporting-modernization/) | Re-engineer fragmented finance reporting into governed reusable layers | Azure Databricks, PySpark, Delta Lake, SQL, Power BI | Complete |
| [FTE Data Platform & Workforce Analytics](projects/fte-workforce-analytics/) | Integrate finance and HR-style sources into governed workforce metrics | ADLS Gen2, ADF, Databricks, PySpark, Delta Lake, Power BI | Complete |
| [FP&A Knowledge Assistant](projects/fpa-knowledge-assistant/) | Ground finance-process answers in approved synthetic SOPs and reporting guides | Azure OpenAI, LangChain, RAG, SharePoint, Streamlit | Complete |
| [Report Navigation & KPI Help Assistant](projects/report-kpi-help-assistant/) | Explain approved KPI logic, ownership, and Power BI report navigation | OpenAI, Power BI, Streamlit, governed KPI catalogue | Complete |
| [Budget Data Integration & Automation](projects/budget-data-integration-automation/) | Automate budget-list ingestion into validated SQL reporting layers | SharePoint, Logic Apps, Azure SQL, Power BI DirectQuery | Complete |
| Streaming Operations Monitor | Detect operational anomalies from event streams and serve near-real-time metrics | Spark Structured Streaming, Delta Lake, Power BI | Planned |

## Engineering Principles

- Incremental and idempotent processing
- Explicit data-quality checks and quarantine handling
- Business-ready dimensional outputs
- Secure configuration with no committed secrets
- Automated tests and CI validation
- Clear architecture and operational documentation

## Repository Structure

```text
projects/   Portfolio projects and documentation
.github/    Continuous-integration workflows
```

## Contact

- GitHub: [Shashidhara-KB](https://github.com/Shashidhara-KB)
- Focus: Data Engineer / GenAI Engineer
