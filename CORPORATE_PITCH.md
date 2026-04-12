# Corporate Pitch – AI-Powered PPT Generator

> **How to use this document:**  Fill in the sections marked `[YOUR …]` with
> numbers from your own organisation, then share with your manager or budget
> holder.

---

## Executive Summary

We have identified and tested an AI-powered PowerPoint generation tool that
reduces presentation creation time by **[YOUR: 60–80]%** per document.

The solution was validated in-house using its built-in demo mode (zero cost)
and a small-scale trial with the Anthropic Claude API free credit.

We are requesting approval to deploy it at scale.

---

## The Problem

| Pain Point | Current State |
|------------|--------------|
| Time to create a 10-slide deck | **[YOUR: X hours]** |
| Number of presentations per month (team) | **[YOUR: X]** |
| Total hours lost on slide creation/month | **[YOUR: X hours]** |
| Estimated cost at **[YOUR: $Y/hour]** loaded rate | **$[YOUR: calculated]** |

> **Example:** 20 presentations/month × 3 hours each × $75/hour = **$4,500/month**
> in labour spent on formatting slides rather than delivering value.

---

## The Solution

**PPT Generator** is a FastAPI-based backend service that:

1. Accepts a plain-English prompt
2. Calls an LLM (Claude / open-source) to generate structured slide content
3. Produces a fully formatted `.pptx` file in seconds
4. Supports custom templates and style themes

**Key capabilities:**
- Generate a 10-slide presentation in **under 60 seconds**
- Transform existing PowerPoint files into reusable templates
- REST API integrates with any internal portal or productivity tool
- Self-hosted – your data never leaves company infrastructure (optional)
- Demo Mode for risk-free evaluation (no API key required)

---

## Free Trial Results

*Complete this section after running the Demo Mode and/or free API trial.*

| Metric | Result |
|--------|--------|
| Number of test presentations generated | [YOUR: X] |
| Average generation time | [YOUR: X seconds] |
| Presentation quality (1-5 scale, team rating) | [YOUR: X/5] |
| Time saved vs manual creation | [YOUR: X%] |
| Issues encountered | [YOUR: none / list] |
| Team feedback summary | [YOUR: quotes from colleagues] |

**Sample generated files are attached** (see `generated/` folder or shared drive link).

---

## Cost Analysis

### API Costs (Claude)

| Volume | Monthly API Cost |
|--------|-----------------|
| 50 presentations/month | ~$0.50–1.50 |
| 200 presentations/month | ~$2.00–6.00 |
| 500 presentations/month | ~$5.00–15.00 |
| 1 000 presentations/month | ~$10.00–30.00 |

*Costs based on Claude 3.5 Sonnet pricing. Actual cost depends on slide count
and content complexity. See [FREE_TESTING.md](FREE_TESTING.md) for the cost
calculator formula.*

### Hosting Costs

| Option | Monthly Cost |
|--------|-------------|
| Existing server / cloud instance | $0 (use spare capacity) |
| Small cloud VM (2 vCPU, 4 GB RAM) | ~$20–40/month |
| Docker on existing CI/CD infra | $0 |

### Total Cost of Ownership (Year 1)

| Item | Estimated Cost |
|------|---------------|
| API credits (Claude) | $[YOUR: calculated] |
| Hosting | $[YOUR: calculated] |
| Engineering setup (one-time, ~2 days) | $[YOUR: 2 × daily rate] |
| **Total Year 1** | **$[YOUR: sum]** |

---

## ROI Calculation

```
Hours saved/month = presentations/month × hours_saved_per_presentation

Current cost/month = presentations/month × hours_per_deck × hourly_rate

New cost/month    = API cost + hosting cost

Monthly savings   = Current cost/month − New cost/month

Annual ROI (%)    = (Annual savings − Investment) / Investment × 100
```

### Example Calculation

```
20 presentations/month × 2.5 hours saved × $75/hour = $3,750 saved/month

Tool cost: $5 API + $30 hosting = $35/month

Net monthly saving: $3,715
Annual saving:      $44,580
Year 1 investment:  $35 × 12 + $1,200 setup = $1,620

ROI = ($44,580 − $1,620) / $1,620 × 100 = 2,651%
```

*Replace the numbers above with your own to produce a tailored ROI figure.*

---

## Implementation Timeline

```
Week 1: Setup & Integration
  ├─ Deploy Docker container on company server
  ├─ Configure API key and environment variables
  └─ Smoke-test with 5 real presentations

Week 2: Pilot Group
  ├─ Onboard 5-10 early adopters
  ├─ Collect feedback via short survey
  └─ Iterate on prompt templates

Week 3-4: Wider Rollout
  ├─ Open access to full team
  ├─ Integrate with intranet / Slack / Teams (optional)
  └─ Establish usage guidelines

Month 2+: Optimisation
  ├─ Custom templates matching brand guidelines
  ├─ Monitor API costs vs. budget
  └─ Evaluate open-source model option to eliminate API costs
```

---

## Risk & Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| AI generates inaccurate content | Medium | Human review before sharing |
| API costs exceed budget | Low | Usage caps in Anthropic console |
| Data privacy concerns | Medium | Self-hosted deployment option |
| Team adoption | Low | Demo Mode for zero-risk onboarding |
| Vendor dependency | Low | Open-source fallback (Ollama) |

---

## Alternatives Considered

| Option | Cost | Quality | Effort |
|--------|------|---------|--------|
| Manual creation (status quo) | High (labour) | Variable | High |
| Microsoft 365 Copilot | $30/user/month | Good | Low |
| PowerPoint Designer (built-in) | Included in M365 | Limited | Low |
| **PPT Generator (this proposal)** | **<$1/100 decks** | **Excellent** | **Low** |
| Custom in-house build | High (dev cost) | Variable | Very High |

---

## Recommendation

**Approve a 90-day pilot** with:

- Budget: **$[YOUR: calculated] for API credits + hosting**
- Team: **[YOUR: N] users** in **[YOUR: department/team]**
- Success criteria:
  - ≥ 50% reduction in slide creation time
  - Team satisfaction score ≥ 4/5
  - Total cost < $[YOUR: budget cap]

---

## Appendix

### A. Technical Stack

| Component | Technology |
|-----------|-----------|
| Backend API | Python / FastAPI |
| LLM | Anthropic Claude 3.5 Sonnet (or open-source) |
| File generation | python-pptx |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Deployment | Docker / Docker Compose |

### B. Security & Compliance

- API keys stored in environment variables (not in code)
- No presentation content is logged or retained by the API provider beyond
  standard data-processing agreements
- Self-hosted option available for maximum data control
- CORS and input validation built-in

### C. Contact & Repository

- Repository: [github.com/NeelThomas1902/ppt-generator](https://github.com/NeelThomas1902/ppt-generator)
- Free testing guide: [FREE_TESTING.md](FREE_TESTING.md)
- Prepared by: **[YOUR NAME]**, **[YOUR ROLE]**, **[DATE]**
