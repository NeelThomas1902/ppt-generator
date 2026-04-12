"""Mock LLM service for demo/testing without any API key or costs.

Enable by setting ``DEMO_MODE=true`` in your ``.env`` file.
"""

from __future__ import annotations

import asyncio
import random
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# Canned slide-deck templates – realistic enough to demo the full pipeline
# ---------------------------------------------------------------------------

_MOCK_DECKS: list[Dict[str, Any]] = [
    {
        "title": "Introduction to Artificial Intelligence",
        "slides": [
            {
                "title": "What Is Artificial Intelligence?",
                "content": [
                    "AI simulates human intelligence in machines",
                    "Enables computers to learn, reason, and problem-solve",
                    "Powers everyday tools: search engines, voice assistants, recommendations",
                ],
                "notes": "Start with a relatable example such as a smartphone assistant.",
                "layout": "title",
            },
            {
                "title": "Key AI Branches",
                "content": [
                    "Machine Learning – learns from data",
                    "Natural Language Processing – understands text and speech",
                    "Computer Vision – interprets images and video",
                    "Robotics – physical interaction with the world",
                ],
                "notes": "Brief overview; each branch will be explored in subsequent slides.",
                "layout": "content",
            },
            {
                "title": "Machine Learning Fundamentals",
                "content": [
                    "Supervised learning: labelled training data",
                    "Unsupervised learning: finds hidden patterns",
                    "Reinforcement learning: learns via rewards and penalties",
                    "Deep learning: multi-layer neural networks",
                ],
                "notes": "Use the analogy of teaching a child to read.",
                "layout": "content",
            },
            {
                "title": "Real-World AI Applications",
                "content": [
                    "Healthcare: early disease detection and drug discovery",
                    "Finance: fraud detection and algorithmic trading",
                    "Transportation: autonomous vehicles and route optimisation",
                    "Retail: personalised recommendations and inventory management",
                ],
                "notes": "Include a short case study for each sector.",
                "layout": "content",
            },
            {
                "title": "Challenges & Ethical Considerations",
                "content": [
                    "Bias in training data leading to unfair outcomes",
                    "Privacy and data security concerns",
                    "Job displacement and workforce impact",
                    "Transparency and explainability of AI decisions",
                ],
                "notes": "Acknowledge trade-offs; invite audience discussion.",
                "layout": "content",
            },
            {
                "title": "The Future of AI",
                "content": [
                    "General AI vs narrow AI – where are we heading?",
                    "Human-AI collaboration as the dominant paradigm",
                    "Estimated $15.7 trillion economic contribution by 2030",
                    "Governance frameworks and international cooperation",
                ],
                "notes": "End on an optimistic but balanced note.",
                "layout": "content",
            },
            {
                "title": "Getting Started with AI",
                "content": [
                    "Free learning resources: Coursera, fast.ai, Kaggle",
                    "Open-source frameworks: TensorFlow, PyTorch, Scikit-learn",
                    "Cloud AI services: AWS, Azure, Google Cloud",
                    "Community: Hugging Face, GitHub, AI research papers",
                ],
                "notes": "Provide direct links in the handout version.",
                "layout": "content",
            },
            {
                "title": "Key Takeaways",
                "content": [
                    "AI is already transforming every industry",
                    "Multiple branches serve different use-cases",
                    "Ethical AI requires intentional design",
                    "Now is the best time to start learning AI",
                ],
                "notes": "Summarise and open the floor for questions.",
                "layout": "title",
            },
        ],
    },
    {
        "title": "Digital Transformation Strategy",
        "slides": [
            {
                "title": "Why Digital Transformation Matters",
                "content": [
                    "70% of companies report accelerated digital adoption post-2020",
                    "Customers expect seamless digital experiences",
                    "Competitors are modernising at record speed",
                ],
                "notes": "Frame as urgency, not just opportunity.",
                "layout": "title",
            },
            {
                "title": "Current State Assessment",
                "content": [
                    "Legacy systems slow innovation and increase costs",
                    "Siloed data limits insight-driven decisions",
                    "Manual processes reduce efficiency",
                    "Talent gap in digital skills",
                ],
                "notes": "Reference internal audit findings here.",
                "layout": "content",
            },
            {
                "title": "Transformation Pillars",
                "content": [
                    "Customer Experience – omnichannel journeys",
                    "Operational Excellence – automation and optimisation",
                    "Data & Analytics – real-time intelligence",
                    "Culture & People – agile mindsets",
                ],
                "notes": "Each pillar will be addressed in dedicated workstreams.",
                "layout": "content",
            },
            {
                "title": "Technology Roadmap",
                "content": [
                    "Phase 1 (0-6 months): Foundation – cloud migration & API layer",
                    "Phase 2 (6-18 months): Integration – unified data platform",
                    "Phase 3 (18-36 months): Intelligence – AI/ML capabilities",
                ],
                "notes": "Show Gantt chart in appendix.",
                "layout": "content",
            },
            {
                "title": "Investment & ROI",
                "content": [
                    "Estimated investment: $2.5M over 3 years",
                    "Projected cost savings: $1.2M/year by Year 2",
                    "Revenue uplift from new digital channels: $800K/year",
                    "Break-even point: Month 22",
                ],
                "notes": "Detailed financial model available on request.",
                "layout": "content",
            },
            {
                "title": "Risk & Mitigation",
                "content": [
                    "Change resistance – executive sponsorship and training",
                    "Integration complexity – phased approach with rollback plans",
                    "Data security – zero-trust architecture from Day 1",
                    "Vendor lock-in – open standards and multi-cloud strategy",
                ],
                "notes": "Risk register maintained in project management tool.",
                "layout": "content",
            },
            {
                "title": "Success Metrics",
                "content": [
                    "Customer satisfaction score (CSAT) ≥ 4.5/5",
                    "Process automation rate ≥ 60%",
                    "Time-to-market for new features reduced by 40%",
                    "Data-driven decision rate ≥ 80%",
                ],
                "notes": "Review KPIs quarterly; adjust targets as needed.",
                "layout": "content",
            },
            {
                "title": "Next Steps & Call to Action",
                "content": [
                    "Approve budget and form steering committee",
                    "Appoint Chief Digital Officer",
                    "Kick off Phase 1 discovery sprint",
                    "Communicate vision to all employees",
                ],
                "notes": "Request formal sign-off by end of this meeting.",
                "layout": "title",
            },
        ],
    },
    {
        "title": "Product Launch Plan",
        "slides": [
            {
                "title": "Product Vision",
                "content": [
                    "Solving a real pain point for 50M+ potential users",
                    "Best-in-class UX built on user research",
                    "Sustainable competitive moat through data network effects",
                ],
                "notes": "Tell the founding story briefly.",
                "layout": "title",
            },
            {
                "title": "Market Opportunity",
                "content": [
                    "Total addressable market: $8.5B",
                    "Serviceable addressable market: $1.2B",
                    "Initial target segment: SMBs with 10-200 employees",
                    "Compound annual growth rate: 22%",
                ],
                "notes": "Source: Gartner 2024 Market Report.",
                "layout": "content",
            },
            {
                "title": "Competitive Landscape",
                "content": [
                    "Incumbent A: high price, poor UX",
                    "Incumbent B: feature-rich but complex",
                    "Our positioning: simple, affordable, delightful",
                    "Key differentiator: AI-powered automation saves 5h/week",
                ],
                "notes": "Competitive matrix available in appendix.",
                "layout": "two_column",
            },
            {
                "title": "Go-to-Market Strategy",
                "content": [
                    "Product-led growth: freemium to convert self-serve users",
                    "Content marketing & SEO for organic acquisition",
                    "Strategic partnerships with industry influencers",
                    "Targeted paid ads for high-intent segments",
                ],
                "notes": "CAC target: <$50; LTV target: >$800.",
                "layout": "content",
            },
            {
                "title": "Launch Timeline",
                "content": [
                    "Month 1-2: Closed beta with 100 design partners",
                    "Month 3: Open beta & waitlist campaign",
                    "Month 4: Public launch with PR push",
                    "Month 6: First enterprise tier available",
                ],
                "notes": "Beta feedback loop is critical – weekly retrospectives.",
                "layout": "content",
            },
            {
                "title": "Revenue Model",
                "content": [
                    "Free tier: up to 3 users, core features",
                    "Pro: $29/month per team, advanced features",
                    "Business: $99/month, unlimited users + integrations",
                    "Enterprise: custom pricing, SLA & dedicated support",
                ],
                "notes": "Annual discount of 20% drives higher LTV.",
                "layout": "content",
            },
            {
                "title": "Year 1 Targets",
                "content": [
                    "10,000 registered users by Month 6",
                    "1,000 paying customers by Month 12",
                    "$500K ARR by end of Year 1",
                    "NPS ≥ 60",
                ],
                "notes": "Board milestone for Series A readiness.",
                "layout": "content",
            },
            {
                "title": "Team & Resources",
                "content": [
                    "Founding team: 3 engineers, 1 designer, 1 growth lead",
                    "Hiring plan: 5 additional engineers in Q2",
                    "Current runway: 18 months",
                    "Advisory board: 3 industry veterans",
                ],
                "notes": "Org chart appended.",
                "layout": "title",
            },
        ],
    },
]


def _pick_deck(prompt: str, slide_count: int) -> Dict[str, Any]:
    """Return a mock deck that loosely matches the prompt and slide count."""
    # Simple keyword matching to pick the most relevant template
    prompt_lower = prompt.lower()
    scores = []
    keywords = [
        {"ai", "artificial", "machine", "learning", "neural", "deep"},
        {"digital", "transform", "strategy", "enterprise", "cloud"},
        {"product", "launch", "market", "startup", "saas", "growth"},
    ]
    for i, kw_set in enumerate(keywords):
        score = sum(1 for k in kw_set if k in prompt_lower)
        scores.append((score, i))

    best_idx = max(scores, key=lambda x: x[0])[1]
    if scores[best_idx][0] == 0:
        best_idx = random.randint(0, len(_MOCK_DECKS) - 1)

    deck = _MOCK_DECKS[best_idx]

    # Adjust slide count
    slides = deck["slides"]
    if slide_count < len(slides):
        slides = slides[:slide_count]
    elif slide_count > len(slides):
        # Pad with extra slides
        extra = slide_count - len(slides)
        for i in range(extra):
            slides = slides + [
                {
                    "title": f"Additional Insights {i + 1}",
                    "content": [
                        "Key finding from our research",
                        "Actionable recommendation",
                        "Expected outcome and timeline",
                    ],
                    "notes": "Expand based on audience questions.",
                    "layout": "content",
                }
            ]

    return {"title": deck["title"], "slides": slides}


class MockLLMService:
    """Drop-in replacement for :class:`LLMService` that never calls any API.

    All responses are generated locally from pre-built templates so the
    entire presentation pipeline can be exercised for free.
    """

    async def generate_presentation_content(
        self,
        prompt: str,
        slide_count: int = 8,
        theme: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return a realistic fake presentation without any API call."""
        # Simulate a brief network delay so the UI behaves realistically
        await asyncio.sleep(0.5)
        return _pick_deck(prompt, slide_count)

    async def improve_slide_content(
        self,
        slide_content: Dict[str, Any],
        instructions: str,
    ) -> Dict[str, Any]:
        """Return a lightly modified version of the slide without any API call."""
        await asyncio.sleep(0.2)
        improved = dict(slide_content)
        # Append a note so the user can see the mock is working
        improved["notes"] = (
            (improved.get("notes") or "")
            + f" [DEMO: would apply – {instructions}]"
        ).strip()
        return improved
