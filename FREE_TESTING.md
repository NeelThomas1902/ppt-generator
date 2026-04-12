# Free Testing Guide

Test the PPT Generator completely for free before committing to any paid API plan.
This guide covers three approaches in order from **easiest** to **most involved**.

---

## Option 1 – Demo Mode (No API Key, No Cost) ⭐ Recommended

The application ships with a built-in **mock LLM service** that returns realistic
presentation content without ever calling an external API.

### Quick Start

```bash
# 1. Clone the repository (if you haven't already)
git clone https://github.com/NeelThomas1902/ppt-generator.git
cd ppt-generator

# 2. Create a virtual environment and install dependencies
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt

# 3. Create a .env file with DEMO_MODE enabled
cp .env.example .env
# Open .env and set:  DEMO_MODE=true

# 4. Start the server
uvicorn app.main:app --reload
```

The server starts at **http://localhost:8000**.
Open **http://localhost:8000/docs** for the interactive Swagger UI.

### Demo Mode via Docker (One Command)

```bash
docker compose -f docker-compose-demo.yml up --build
```

No `.env` file needed – everything is pre-configured.

### What Demo Mode Does

| Feature | Demo Mode |
|---------|-----------|
| Generate presentations | ✅ Uses pre-built realistic mock data |
| Upload & transform templates | ✅ Full pipeline works |
| Download `.pptx` files | ✅ Real PPTX files are created |
| API key required | ❌ Not needed |
| Internet connection required | ❌ Fully offline |
| Cost | **$0** |

> **Note:** Mock responses are chosen based on your prompt keywords (AI, digital
> transformation, product launch, etc.). The resulting `.pptx` files are real and
> can be opened in PowerPoint or LibreOffice.

---

## Option 2 – Anthropic Free Trial ($5 Credit)

Anthropic offers a **$5 free credit** on sign-up – enough for ~100–500 real
presentation generations depending on slide count.

### Step-by-Step

1. **Create an account** at [console.anthropic.com](https://console.anthropic.com/)
2. Verify your email address
3. Navigate to **API Keys** → **Create Key**
4. Copy the key (it starts with `sk-ant-…`)
5. Add it to your `.env` file:

```env
DEMO_MODE=false
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

6. Restart the server – you are now using real Claude responses

### Estimated Free-Tier Usage

| Action | Approximate tokens | Approximate cost |
|--------|--------------------|------------------|
| 10-slide presentation | ~2 000 tokens | ~$0.01–0.03 |
| Improve a single slide | ~500 tokens | ~$0.002 |
| 50 test generations | ~100 000 tokens | ~$0.50–1.50 |

Your **$5 credit** covers significant testing before any charges apply.

---

## Option 3 – Open-Source / Self-Hosted LLMs (Free Forever)

Run a local language model instead of calling any external API.

### Option 3a – Ollama + LLaMA / Mistral

[Ollama](https://ollama.ai) lets you run powerful open-source models on your
own machine.

**Requirements:** 8 GB RAM minimum (16 GB recommended for best quality)

```bash
# 1. Install Ollama
#    Download from https://ollama.ai/download  or:
curl -fsSL https://ollama.ai/install.sh | sh   # Linux / macOS

# 2. Pull a model
ollama pull mistral          # ~4 GB – fast and capable
# or
ollama pull llama2           # ~3.8 GB
# or
ollama pull llama3           # ~4.7 GB – best quality

# 3. Start Ollama
ollama serve
# Ollama API is now at http://localhost:11434
```

**Integrate with ppt-generator:**

Ollama exposes an OpenAI-compatible REST API. You can point the application at
it by creating a thin adapter or by swapping the Anthropic client for the
`openai` library:

```python
# In app/services/llm_service.py  (or a new file)
import openai

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",            # any non-empty string
)
response = client.chat.completions.create(
    model="mistral",
    messages=[{"role": "user", "content": your_prompt}],
)
```

> **Tip:** For quick testing keep `DEMO_MODE=true`; switch to Ollama only when
> you want AI-generated (non-mock) content without paying for an API.

### Option 3b – Google Gemini Free Tier

Google's Gemini API offers a generous free tier (60 requests/minute as of 2024)
via [Google AI Studio](https://aistudio.google.com/).

1. Sign in with your Google account at **aistudio.google.com**
2. Click **Get API key** → **Create API key**
3. Adapt the LLM service to use `google-generativeai` package

### Option 3c – OpenAI-Compatible Providers

Many providers offer free tiers with OpenAI-compatible APIs:

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| Groq | 14 400 req/day | Very fast inference |
| Together AI | $25 credit | Many open models |
| Fireworks AI | $1 credit | Fast & cheap |
| Hugging Face Inference API | Limited free | Many models |

---

## Comparison Table

| Option | Cost | Setup Time | Response Quality | Internet Required |
|--------|------|------------|-----------------|-------------------|
| Demo Mode | $0 | 2 minutes | Mock data | No |
| Anthropic Free Trial | $0 (first $5) | 5 minutes | Excellent | Yes |
| Ollama (Mistral) | $0 | 15 minutes | Very good | No (after download) |
| Ollama (LLaMA 3) | $0 | 20 minutes | Excellent | No (after download) |
| Anthropic Paid | ~$0.01/gen | 5 minutes | Excellent | Yes |

---

## Cost Calculator

Use this formula to estimate monthly costs when moving to paid Claude:

```
Monthly cost = (presentations/day × slides/presentation × avg_tokens_per_slide × days/month)
               × price_per_token

Example (50 presentations/day, 10 slides, ~300 tokens/slide):
  = 50 × 10 × 300 × 30 × $0.000003
  ≈ $1.35/month
```

For most teams generating fewer than 200 presentations/day the monthly cost is
**under $5** – much less than the time saved per presentation.

---

## Recommended Testing Workflow

```
Week 1 – Proof of Concept
  └─ DEMO_MODE=true
     ✓ Run through all API endpoints
     ✓ Verify .pptx files open correctly
     ✓ Demo to stakeholders

Week 2 – Real AI Quality
  └─ Anthropic free trial ($5 credit)
     ✓ Generate 20-30 real presentations
     ✓ Evaluate output quality
     ✓ Gather user feedback

Week 3 – Corporate Pitch
  └─ Use results from Week 1 & 2
     ✓ Show CORPORATE_PITCH.md to decision makers
     ✓ Request budget approval
     ✓ Implement at scale
```

---

## Troubleshooting

**`ANTHROPIC_API_KEY` not set error in Demo Mode**

Make sure `DEMO_MODE=true` is in your `.env` file and restart the server.

**Mock responses always return the same presentation**

Demo Mode picks templates based on prompt keywords. Try prompts containing words
like "AI", "digital transformation", or "product launch" for different results.

**Server won't start – port 8000 in use**

```bash
# Change the port
uvicorn app.main:app --reload --port 8001
```

---

## Next Steps

Once you have validated the project with free testing, see
[CORPORATE_PITCH.md](CORPORATE_PITCH.md) for a ready-made template to present
the business case to your organisation.
