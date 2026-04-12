# ppt-generator

An AI-powered PowerPoint presentation generator built with FastAPI and Claude.

---

## Quick Start

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
# Windows: python -m uvicorn app.main:app --reload
```

The API is now available at **http://localhost:8000**.  
Interactive docs (Swagger UI): **http://localhost:8000/docs**

### 5. Make your first request

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Introduction to renewable energy", "slide_count": 5}'
```

---

## Docker

```bash
cp .env.example .env   # add your API key
docker-compose up --build
```

---

## Documentation

- 📖 [API Documentation](API_DOCUMENTATION.md) — full endpoint reference, request/response examples, error codes
- 🚀 [Quick Start Guide](QUICKSTART.md) — step-by-step setup, common errors and solutions

---

## Examples

The [`examples/`](examples/) directory contains ready-to-run scripts:

| File | Description |
|------|-------------|
| [`examples/generate_ppt.py`](examples/generate_ppt.py) | Generate a presentation from a text prompt |
| [`examples/transform_ppt.py`](examples/transform_ppt.py) | Upload and transform an existing `.pptx` into a template |
| [`examples/curl_requests.sh`](examples/curl_requests.sh) | Shell script covering all API endpoints with curl |

---

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Available Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/generate` | Generate a PPT from a text prompt |
| `POST` | `/api/v1/transform` | Convert an existing PPT into a template |
| `POST` | `/api/v1/upload-template` | Upload a JSON template definition |
| `GET` | `/api/v1/templates` | List all saved templates |
| `GET` | `/api/v1/presentation/{id}` | Get a presentation by ID |