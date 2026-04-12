# 🔑 API Keys Setup Guide

This guide explains how to obtain, configure, and secure your Anthropic Claude API key for the PPT Generator.

---

## 1. Get Your Claude API Key

### Step 1 — Create an Anthropic Account

1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Click **Sign up** (or **Log in** if you already have an account)
3. Verify your email address

### Step 2 — Add a Payment Method (if needed)

1. After signing in, navigate to **Billing** in the left sidebar
2. Add a credit card to activate your account
3. New accounts typically receive **$5 in free credits** — no charge until credits are exhausted

### Step 3 — Generate an API Key

1. Go to **API Keys** in the left sidebar of the Console
2. Click **Create Key**
3. Give it a descriptive name (e.g. `ppt-generator-dev`)
4. **Copy the key immediately** — it is only shown once!

> ⚠️ If you lose the key, you must create a new one. The old key cannot be recovered.

---

## 2. Configure the API Key in Your Project

### Option A — Using `.env` file (recommended for local development)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor and replace the placeholder:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
   ```

3. Save the file. The application reads this automatically on startup.

### Option B — Setting an environment variable directly

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-YOUR_ACTUAL_KEY_HERE"
uvicorn app.main:app --reload
```

**macOS / Linux (Bash):**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-YOUR_ACTUAL_KEY_HERE"
uvicorn app.main:app --reload
```

### Option C — Docker / docker-compose

Add the key to your `.env` file (which `docker-compose.yml` reads automatically via `env_file: .env`):
```env
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
```

Then run:
```bash
docker-compose up --build
```

---

## 3. Verify the Key Is Working

Start the server and call the health endpoint:
```bash
curl http://localhost:8000/health
```

Then try generating a simple presentation:
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A 3-slide intro to Python programming"}'
```

If you see a `500` error mentioning authentication, double-check that `ANTHROPIC_API_KEY` is set correctly.

---

## 4. Security Best Practices

### ✅ Do

- Store the API key **only** in `.env` (never hard-code it in source files)
- Add `.env` to `.gitignore` — it is already excluded in this project
- Rotate keys periodically (every 90 days is a good practice)
- Use separate keys for development and production environments
- Set **spending limits** in the Anthropic Console to cap unexpected charges

### ❌ Don't

- Commit the `.env` file to Git
- Share the key in Slack, emails, or screenshots
- Embed the key in frontend JavaScript (it would be publicly visible)
- Use the same key for multiple unrelated projects

### Checking that `.env` is ignored

```bash
git check-ignore -v .env
# Expected output: .gitignore:1:.env  .env
```

---

## 5. Setting Up Cost Alerts

To avoid unexpected charges:

1. Log in to [https://console.anthropic.com](https://console.anthropic.com)
2. Go to **Billing → Usage Limits**
3. Set a **Soft limit** (sends an email warning) — e.g. `$5`
4. Set a **Hard limit** (stops all API calls) — e.g. `$10`

This ensures you never accidentally spend more than your hard limit in a single month.

---

## 6. Rotating a Compromised Key

If you accidentally expose your key (e.g. committed to GitHub):

1. Go to **API Keys** in the Anthropic Console
2. Click the three-dot menu next to the compromised key
3. Select **Delete**
4. Create a new key and update your `.env` file immediately
5. Check the **Usage** page for any unexpected activity

---

## 7. Key Format Reference

Anthropic API keys follow this format:

```
sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXX
```

- Always starts with `sk-ant-`
- Never share keys that match this pattern in any public forum

---

## Related Documentation

- [COSTS_AND_PRICING.md](./COSTS_AND_PRICING.md) — pricing breakdown and cost tips
- [Anthropic API Docs](https://docs.anthropic.com) — official reference
- [Anthropic Console](https://console.anthropic.com) — manage keys and billing
