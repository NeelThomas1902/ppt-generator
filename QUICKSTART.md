# Quick Start Guide

Get the PPT Generator API running locally in a few minutes.

---

## Prerequisites

- Python 3.10 or 3.11
- An [Anthropic API key](https://console.anthropic.com/) (for AI generation)

---

## 1. Clone the Repository

```bash
git clone https://github.com/NeelThomas1902/ppt-generator.git
cd ppt-generator
```

---

## 2. Set Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

All other defaults work out of the box for local development.

---

## 5. Run the Server

```bash
uvicorn app.main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Application startup complete.
```

> **Windows users:** If `uvicorn` is not found, use `python -m uvicorn app.main:app --reload`

---

## 6. Verify the Server is Running

Open your browser and visit:

- **Swagger UI (interactive docs):** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

Expected health check response:

```json
{"status": "ok"}
```

---

## 7. Make Your First API Call

### Generate a Presentation

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a presentation about the benefits of renewable energy",
    "slide_count": 5
  }'
```

**Expected response:**

```json
{
  "id": "d3a4b5c6-1234-5678-abcd-ef1234567890",
  "filename": "presentation_d3a4b5c6.pptx",
  "download_url": "/generated/presentation_d3a4b5c6.pptx",
  "slide_count": 5,
  "created_at": "2026-04-12T05:00:00",
  "prompt": "Create a presentation about the benefits of renewable energy"
}
```

### List Available Templates

```bash
curl http://localhost:8000/api/v1/templates
```

**Expected response:**

```json
{
  "templates": [],
  "total": 0
}
```

---

## Docker (Alternative)

If you prefer Docker, you can run the entire stack with one command:

```bash
# Copy the env file first
cp .env.example .env
# Add your API key to .env

# Start with Docker Compose
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

---

## Common Errors and Solutions

### `uvicorn` not found (Windows)

```
uvicorn : The term 'uvicorn' is not recognized...
```

**Fix:** Use the Python module syntax:

```powershell
python -m uvicorn app.main:app --reload
```

Or activate your virtual environment first.

---

### `No module named uvicorn`

```
python.exe: No module named uvicorn
```

**Fix:** You may have multiple Python installations. Create a virtual environment and install dependencies inside it:

```bash
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### AI generation fails (500 error)

```json
{"detail": "Failed to generate presentation. Please try again."}
```

**Fix:** Check that your `ANTHROPIC_API_KEY` is set correctly in `.env` and that the key is valid.

---

### `422 Unprocessable Entity`

```json
{"detail": [{"msg": "String should have at least 10 characters", ...}]}
```

**Fix:** Make sure your `prompt` is at least 10 characters long.

---

## Next Steps

- Read the full [API Documentation](API_DOCUMENTATION.md)
- Explore the [examples/](examples/) directory for Python and shell scripts
- Browse the interactive Swagger UI at http://localhost:8000/docs
