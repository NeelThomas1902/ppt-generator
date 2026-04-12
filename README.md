# 🎯 PPT Generator

AI-powered PowerPoint presentation generator built with **FastAPI** and **Claude (Anthropic)**.

---

## ✨ Features

- 🤖 Generate presentations from natural-language prompts using Claude AI
- 🔄 Transform existing `.pptx` files into reusable templates
- 📂 Upload and manage JSON template definitions
- 🖥️ Built-in web UI — no extra tools needed
- ⬇️ Download generated presentations directly from the browser

---

## 🖥️ Web UI

The application includes a built-in frontend served at **`http://localhost:8000`**.

| Tab | What it does |
|---|---|
| ✨ Generate PPT | Enter a prompt, choose slides & theme, click Generate |
| 🔄 Transform PPT | Upload a `.pptx` to create a reusable template |
| 📂 Templates | Upload JSON templates or browse saved ones |
| ⬇️ My Presentations | Retrieve & download past presentations by ID |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (or Docker)
- An Anthropic API key → see [API_KEYS.md](./API_KEYS.md)

### 1. Clone the repository

```bash
git clone https://github.com/NeelThomas1902/ppt-generator.git
cd ppt-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Open **http://localhost:8000** in your browser to use the UI.

---

## 🐳 Docker

```bash
# Copy and edit .env first
cp .env.example .env

docker-compose up --build
```

The UI will be available at **http://localhost:8000**.

---

## 📡 API Endpoints

All endpoints are prefixed with `/api/v1`.

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/generate` | Generate a PPT from a text prompt |
| `POST` | `/api/v1/transform` | Convert a `.pptx` file into a template |
| `POST` | `/api/v1/upload-template` | Upload a JSON template definition |
| `GET` | `/api/v1/templates` | List all saved templates |
| `GET` | `/api/v1/presentation/{id}` | Get metadata for a generated presentation |
| `GET` | `/health` | Health check |

Interactive API docs are available at **http://localhost:8000/docs**.

---

## 🧪 Running Tests

```bash
pytest -v
```

---

## 📚 Documentation

| File | Description |
|---|---|
| [API_KEYS.md](./API_KEYS.md) | How to get and configure your Claude API key |
| [COSTS_AND_PRICING.md](./COSTS_AND_PRICING.md) | Claude API pricing, cost examples, and tips |

---

## 💰 API Costs

This project uses the Claude API which is a **paid service** (with free trial credits).

- New accounts get **~$5 in free credits**
- A typical 10-slide presentation costs less than **$0.01** with Claude 3 Haiku
- See [COSTS_AND_PRICING.md](./COSTS_AND_PRICING.md) for a full breakdown

---

## 🔧 Environment Variables

| Variable | Description | Default |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Claude API key (**required**) | — |
| `APP_HOST` | Server bind address | `0.0.0.0` |
| `APP_PORT` | Server port | `8000` |
| `DATABASE_URL` | SQLite/PostgreSQL URL | SQLite (local) |
| `UPLOAD_DIR` | Directory for uploaded files | `uploads` |
| `TEMPLATES_DIR` | Directory for built-in templates | `app/templates` |
| `MAX_UPLOAD_SIZE_MB` | Max upload size | `50` |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:3000,...` |

---

## 📁 Project Structure

```
ppt-generator/
├── app/
│   ├── api/          # Routes and schemas
│   ├── models/       # Database models
│   ├── services/     # LLM, PPT generation, templates
│   ├── utils/        # File handlers, validators
│   ├── config.py     # Settings
│   ├── database.py   # DB connection
│   └── main.py       # App entry point
├── frontend/
│   └── index.html    # Web UI
├── tests/            # Test suite
├── API_KEYS.md
├── COSTS_AND_PRICING.md
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```