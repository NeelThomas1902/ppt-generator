# Testing Guide

This document explains how to run, extend and interpret the ppt-generator test suite.

---

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1

# 2. Install all dependencies (includes pytest, pytest-asyncio, httpx)
pip install -r requirements.txt
pip install pytest-cov             # optional – for coverage reports

# 3. Run every test
pytest
```

---

## Test layout

```
tests/
├── __init__.py           # makes tests a package
├── conftest.py           # shared fixtures (client, mock LLM, sample data)
├── test_api.py           # API endpoint smoke tests
├── test_services.py      # unit tests for validators and utilities
└── test_integration.py   # end-to-end workflow tests
```

### `tests/conftest.py`

Provides reusable pytest fixtures available to every test module:

| Fixture | Description |
|---|---|
| `client` | `TestClient` wrapping the FastAPI application |
| `mock_llm_content` | Pre-built presentation content dict (no API key needed) |
| `mock_llm_service` | Patches `LLMService` so no real Anthropic call is made |
| `sample_template_dict` | Minimal valid template definition dict |
| `sample_template_bytes` | JSON-encoded bytes of `sample_template_dict` |
| `valid_pptx_bytes` | Bytes of an empty but structurally valid `.pptx` file |

### `tests/test_api.py` – API smoke tests

| Test | What it checks |
|---|---|
| `test_health_check` | `GET /health` returns `{"status": "ok"}` |
| `test_generate_rejects_short_prompt` | Prompt < 10 chars → HTTP 422 |
| `test_generate_rejects_missing_prompt` | Missing `prompt` field → HTTP 422 |
| `test_list_templates_returns_list` | `GET /api/v1/templates` returns `{templates, total}` |
| `test_get_presentation_not_found` | Unknown ID → HTTP 404 |
| `test_transform_rejects_non_pptx` | Non-`.pptx` file → HTTP 400 |
| `test_upload_template_rejects_non_json` | Non-`.json` file → HTTP 400 |

### `tests/test_services.py` – Unit tests

| Test | What it checks |
|---|---|
| `test_validate_prompt_raises_on_empty` | Empty prompt raises `ValueError` |
| `test_validate_prompt_raises_on_whitespace` | Whitespace-only prompt raises `ValueError` |
| `test_validate_prompt_raises_on_too_long` | Prompt > 4000 chars raises `ValueError` |
| `test_validate_prompt_passes_valid` | Valid prompt passes without error |
| `test_validate_pptx_accepts_valid_file` | `.pptx` MIME type passes validation |
| `test_validate_pptx_rejects_txt` | `.txt` file raises HTTP 400 |
| `test_validate_pptx_rejects_long_filename` | Filename > 255 chars raises HTTP 400 |
| `test_default_template_is_valid_json` | `default_template.json` parses as valid JSON |
| `test_corporate_theme_is_valid_json` | `corporate_theme.json` parses as valid JSON |

### `tests/test_integration.py` – Integration / workflow tests

| Test | What it checks |
|---|---|
| `test_upload_template_then_list` | Upload JSON template; verify it appears in list |
| `test_upload_minimal_template_without_name` | Template without `name` key falls back to filename |
| `test_generate_presentation_with_mock_llm` | Full generate flow with mocked LLM |
| `test_generate_presentation_returns_valid_response` | Generate response contains required fields |
| `test_generate_with_theme` | `theme` parameter is forwarded without error |
| `test_transform_valid_pptx` | Upload `.pptx`; verify it creates a template record |
| `test_get_nonexistent_presentation_returns_404` | Unknown presentation ID → HTTP 404 |
| `test_generate_llm_failure_returns_500` | LLM error propagates as HTTP 500 |

---

## Running subsets of tests

```bash
# All tests
pytest

# Only API tests
pytest tests/test_api.py

# Only unit tests
pytest tests/test_services.py

# Only integration tests
pytest tests/test_integration.py

# A specific test by name
pytest -k "test_health_check"

# Stop on first failure
pytest -x

# Verbose output
pytest -v
```

---

## Coverage

```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report (opens in browser from htmlcov/index.html)
pytest --cov=app --cov-report=html
```

---

## Using the Makefile

A `Makefile` at the project root provides convenience targets:

```bash
make test               # run all tests
make test-unit          # run unit tests only  (test_services.py)
make test-api           # run API tests only   (test_api.py)
make test-integration   # run integration tests only
make test-coverage      # generate HTML coverage report
make test-fast          # run tests, stop on first failure
```

---

## Writing new tests

### Adding a unit test

Unit tests should go in `tests/test_services.py` and must not hit the database
or the Anthropic API:

```python
from app.utils.validators import validate_prompt

def test_validate_prompt_passes_short_valid():
    validate_prompt("Hello world!")  # should not raise
```

### Adding an API test

API tests use the shared `client` fixture from `conftest.py`:

```python
def test_my_endpoint(client):
    resp = client.get("/api/v1/templates")
    assert resp.status_code == 200
```

### Adding an integration test with mocked LLM

Use the `mock_llm_service` fixture to avoid real API calls:

```python
def test_generate_slide_count(client, mock_llm_service):
    resp = client.post(
        "/api/v1/generate",
        json={"prompt": "History of the internet", "slide_count": 5},
    )
    assert resp.status_code == 201
    mock_llm_service.assert_called_once()
```

---

## Environment variables

Tests use an **in-memory SQLite** database by default
(`sqlite+aiosqlite:///./ppt_generator.db`) and a blank Anthropic API key.
No real API key is needed when the `mock_llm_service` fixture is used.

To point tests at a specific database, set `DATABASE_URL` before running:

```bash
DATABASE_URL=sqlite+aiosqlite:///./test.db pytest
```

---

## Continuous Integration

The test suite runs automatically on every push and pull request via GitHub
Actions. See `.github/workflows/` for the CI configuration.

To reproduce CI locally:

```bash
pip install -r requirements.txt pytest-cov
pytest --cov=app --cov-report=term-missing -v
```
