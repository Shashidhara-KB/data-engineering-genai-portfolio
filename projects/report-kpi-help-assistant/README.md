# KPI Help Service

**Status: Prototype**

This is a small Python service for looking up approved KPI definitions from a JSON catalogue. I built it as a starting point for report-navigation support, where users need a consistent definition, owner and source rather than a newly generated answer.

## What works today

- Loads KPI definitions from `data/kpi_catalog.json`
- Searches approved names and aliases
- Returns the formula, owner, source and refresh information
- Gives a clear unknown-KPI response when no match is found

## What it is not

This version is not a chatbot and does not call an LLM. A future interface could add natural-language questions and Power BI deep links, but the catalogue should remain the source of truth.

## Why this approach

For metric definitions, predictable lookup is often safer than free-form generation. The prototype keeps that boundary clear and can later be used as a controlled tool inside a broader assistant.
