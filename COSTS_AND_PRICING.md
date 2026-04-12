# 💰 API Costs & Pricing

This document explains the costs associated with using the Claude API (Anthropic) to power the PPT Generator.

---

## 📊 Claude API Pricing (as of 2024)

Anthropic charges per **million tokens** processed. Tokens roughly correspond to words — 1 token ≈ 0.75 words, so 1,000 tokens ≈ 750 words.

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| **Claude 3 Haiku** | $0.25 | $1.25 |
| **Claude 3 Sonnet** | $3.00 | $15.00 |
| **Claude 3 Opus** | $15.00 | $75.00 |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 |
| **Claude 3.5 Haiku** | $0.80 | $4.00 |

> **Note:** Prices may change. Always verify at [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing).

---

## 🧮 Cost Per Request — Examples

### Generating a 10-slide presentation

A typical 10-slide presentation request sends roughly:
- **Input:** ~500 tokens (your prompt + system instructions)
- **Output:** ~2,000 tokens (generated slide content)

| Model | Estimated cost |
|---|---|
| Claude 3 Haiku | ~$0.003 (less than 1 cent) |
| Claude 3 Sonnet | ~$0.032 |
| Claude 3 Opus | ~$0.158 |

### Transforming an uploaded PPT

Transformation reads slide text and generates a JSON template:
- **Input:** ~800 tokens
- **Output:** ~1,200 tokens

| Model | Estimated cost |
|---|---|
| Claude 3 Haiku | ~$0.002 |
| Claude 3 Sonnet | ~$0.021 |

### Monthly usage example

If you generate **100 presentations/month** (10 slides each) using **Claude 3 Haiku**:

```
100 requests × $0.003 = ~$0.30 / month
```

That's **30 cents per month** for 100 presentations!

---

## 🆓 Free Trial / Credits

- Anthropic typically provides **$5 in free credits** when you sign up for a new API account.
- With $5 of free credits and Claude 3 Haiku, you can generate approximately **1,600+ presentations**.
- Free credits usually expire after a few months — check your Anthropic Console for expiry dates.

> Sign up at: [https://console.anthropic.com](https://console.anthropic.com)

---

## 📈 How to Monitor Your API Usage

1. **Log in** to the [Anthropic Console](https://console.anthropic.com)
2. Navigate to **Usage** in the left sidebar
3. You will see:
   - Total tokens used (input and output separately)
   - Costs broken down by day / model
   - A usage graph over time

You can also set **spending limits** to prevent unexpected charges:
1. Go to **Billing → Usage Limits** in the console
2. Set a monthly hard limit (e.g. $10) and a soft limit for email alerts (e.g. $5)

---

## 💡 Cost Optimization Tips

### 1. Use Claude 3 Haiku for most tasks
Claude 3 Haiku is **12× cheaper** than Claude 3 Sonnet and still produces excellent presentations. The default model in this project uses the cheapest capable model.

### 2. Keep prompts concise
Shorter prompts mean fewer input tokens. Instead of:
> "Please create a very detailed and comprehensive PowerPoint presentation about the history and evolution of artificial intelligence from its earliest beginnings in the 1950s all the way through to modern large language models."

Use:
> "PPT: History of AI, 1950s to modern LLMs."

### 3. Reduce slide count when possible
Fewer slides = fewer output tokens = lower cost.

### 4. Cache or reuse templates
Once a template is saved (via `/transform` or `/upload-template`), you can reuse it many times without extra API calls.

### 5. Set a budget alert
In the Anthropic Console, set a **soft limit** (email alert) at a comfortable threshold before hitting your hard limit.

---

## 🔐 Billing & Payment

- **Credit card required** after the free trial ends
- Anthropic uses **prepaid credits** — you top up and consume credits
- Invoices are available in the Billing section of the Console
- Supported payment methods: Visa, Mastercard, American Express

---

## ❓ FAQ

**Q: Will I be charged if the generation fails?**
A: You are charged for tokens _sent to_ the API even if the response is an error. Failed requests mid-stream may still incur partial charges.

**Q: Is there a free tier with no expiry?**
A: As of 2024, Anthropic does not offer a permanent free tier. Initial signup credits expire. Check the Console for the latest offers.

**Q: Can I use a different AI provider to avoid costs?**
A: The codebase uses the `anthropic` Python SDK. You could adapt `app/services/llm_service.py` to use an alternative (e.g. OpenAI, Ollama for local inference), but that would require code changes.

**Q: Where can I find the current pricing?**
A: Always check [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing) for the most up-to-date information.
