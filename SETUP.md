# Setup Guide for ppt-generator

This guide explains how to correctly set up your Python environment and run the project.

---

## ⚠️ Common Issue: Multiple Python Installations

If you see an error like this:

```
python.exe: No module named uvicorn
```

even after running `pip install -r requirements.txt`, you likely have **two separate Python installations** on your machine and are using the wrong one.

**Example of what this looks like:**

- Packages installed in: `C:\Users\<you>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\...`
- But running: `C:\Users\<you>\AppData\Local\Programs\Python\Python311\python.exe`

These are completely separate environments — packages installed in one are **not** available in the other.

---

## ✅ Recommended Fix: Use a Virtual Environment

Using a virtual environment is the cleanest solution. It isolates the project's dependencies from your global Python installation.

### Step 1 — Open a terminal in the project folder

In VS Code, open the integrated terminal (`Ctrl+`` `) and make sure you are in the project directory:

```powershell
cd C:\Users\<you>\OneDrive\Documents\AI\ppt-generator
```

### Step 2 — Create a virtual environment

```powershell
python -m venv venv
```

This creates a `venv` folder inside the project with its own isolated Python environment.

### Step 3 — Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

> **Note:** If you get a script execution policy error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

Once activated, your terminal prompt will show `(venv)` at the start.

### Step 4 — Install dependencies

```powershell
pip install -r requirements.txt
```

All packages (including `uvicorn`) will be installed into the virtual environment.

### Step 5 — Set up environment variables

```powershell
copy .env.example .env
```

Open `.env` and fill in your API key and any other required configuration values.

### Step 6 — Run the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

- **API base:** http://localhost:8000
- **Interactive docs (Swagger):** http://localhost:8000/docs

---

## 🔄 Every Time You Return to the Project

Before running the app in a new terminal session, always activate the virtual environment first:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 🐳 Alternative: Docker (No Python setup required)

If you have Docker installed, you can skip all of the above and run:

```powershell
docker-compose up --build
```

This builds and starts the application in a container with all dependencies pre-installed.

---

## 🩺 Troubleshooting

| Problem | Solution |
|---|---|
| `uvicorn` not found | Make sure the virtual environment is activated (`.\venv\Scripts\Activate.ps1`) |
| `No module named uvicorn` | Re-run `pip install -r requirements.txt` inside the activated venv |
| Script execution policy error | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Wrong Python version in venv | Delete `venv` and recreate it using `py -3.11 -m venv venv` (or another version) |
| API key errors on startup | Make sure `.env` exists and contains valid values (copy from `.env.example`) |
