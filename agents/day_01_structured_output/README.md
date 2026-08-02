# Day 01 — Structured Data Extractor

## Overview

This AI Agent extracts structured candidate information from an unstructured resume using LangGraph and Pydantic.

## Features

- LangGraph workflow
- Structured Output
- Pydantic Validation
- Automatic Retry
- Execution Tracking
- Unit Tests
- Docker Support

## Project Flow

Resume

↓

LLM Extraction

↓

Pydantic Validation

↓

Retry (if required)

↓

Structured JSON

## Run

```bash
python -m agents.day_01_structured_output.agent
```

## Tests

```bash
pytest agents/day_01_structured_output/tests/
```