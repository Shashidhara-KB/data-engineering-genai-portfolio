# FP&A Knowledge Assistant

**Status: Prototype**

I started this project to explore a common FP&A support problem: process documents and KPI guidance exist, but users still spend time asking where to find an answer.

The code currently provides a small, dependency-free retriever that ranks local text using token overlap and cosine similarity. It is useful for testing retrieval behaviour, but it is **not yet** an Azure OpenAI, LangChain or production RAG application.

## What is implemented

- Text tokenization and term-frequency vectors
- Cosine-similarity ranking
- A minimum evidence threshold
- An unsupported-answer path when retrieval confidence is too low

## Planned next step

The next version will add synthetic SOP documents, embeddings, a vector index, answer generation with citations, a small Streamlit interface and retrieval evaluation tests.

A production design would also require document permissions, secret management, prompt-injection controls, logging and a defined review process for source documents.

## Why this project is here

It shows the retrieval foundation and the direction of the solution without claiming that the full GenAI application has already been built.
