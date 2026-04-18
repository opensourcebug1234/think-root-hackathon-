# =============================================================================
# ICP Configuration for P95.AI Lead Scoring
# All weights sum to 100 and mirror the repo's current ICP document.
# The scorer can use richer optional fields when present, while still scoring
# the existing CSV schema using tech-stack and recent-trigger proxies.
# =============================================================================

ICP_CRITERIA = {
    "ai_in_production": {
        "weight": 20,
        "description": "Evidence the company is running AI features in production",
        "managed_platform_signals": [
            "aws bedrock", "vertex ai", "azure openai", "azure ai foundry",
            "openai", "anthropic", "cohere", "together ai", "fireworks",
            "replicate", "hugging face", "sagemaker"
        ],
        "framework_signals": [
            "langchain", "llamaindex", "pytorch", "tensorflow", "ray", "mlflow"
        ],
        "production_keywords": [
            "launched", "general availability", "ga", "production", "in prod",
            "copilot", "assistant", "agent", "rag", "ai product"
        ],
    },
    "inference_scale_complexity": {
        "weight": 15,
        "description": "Signals that inference is a scaled platform problem",
        "serving_signals": [
            "vllm", "triton", "ray", "ray serve", "kserve", "kubernetes",
            "gpu", "cuda", "sagemaker", "vertex ai", "aws bedrock"
        ],
        "complexity_keywords": [
            "latency", "p95", "p99", "throughput", "routing", "fallback",
            "cache", "caching", "gpu", "inference", "scale", "cost"
        ],
    },
    "ai_observability_maturity": {
        "weight": 10,
        "description": "Signals the team already monitors and debugs AI systems",
        "signals": [
            "langsmith", "datadog", "llm observability", "opentelemetry",
            "otel", "mlflow", "weights & biases", "wandb"
        ],
        "keywords": [
            "observability", "monitoring", "reliability", "incident", "sla",
            "uptime", "latency", "degraded", "postmortem", "evaluation", "evals"
        ],
    },
    "ai_job_postings": {
        "weight": 10,
        "description": "Active hiring for AI, platform, or infrastructure roles",
    },
    "headcount_fit": {
        "weight": 10,
        "description": "Enterprise sweet spot is 200-3,000 employees",
        "scoring": {
            "400_2000": 10,
            "200_399": 7,
            "2001_3000": 7,
            "3001_10000": 5,
            "100_199": 3,
            "10001_plus": 3,
            "0_99": 0,
        },
    },
    "arr_monetization_pressure": {
        "weight": 10,
        "description": "Meaningful revenue scale or visible AI monetization pressure",
        "scoring_millions": {
            "50_250": 10,
            "20_49": 8,
            "251_500": 8,
            "500_plus": 7,
            "10_19": 4,
            "0_9": 0,
        },
        "trigger_keywords": {
            "launch": 7,
            "monetization": 7,
            "margin": 7,
            "enterprise": 6,
            "proxy": 4,
        },
    },
    "funding_stage": {
        "weight": 8,
        "description": "Funding stage determines budget availability",
        "scoring": {
            "series_b": 8,
            "series_c": 8,
            "series_a": 7,
            "growth": 7,
            "series_d": 6,
            "series_e": 6,
            "public": 4,
            "seed": 2,
            "pre_seed": 0,
            "bootstrapped": 0,
            "unknown": 0,
        },
    },
    "business_urgency": {
        "weight": 7,
        "description": "Recent funding or trigger event creates urgency",
        "recency_scoring": {
            "0_9": 7,
            "10_18": 4,
            "19_30": 2,
            "31_plus": 0,
        },
        "trigger_keywords": {
            "incident": 7,
            "launch": 5,
            "hiring": 5,
            "leadership": 4,
            "growth": 4,
        },
    },
    "industry_fit": {
        "weight": 5,
        "description": "Industry vertical alignment to P95.AI target markets",
        "scoring": {
            "ai": 5,
            "ml": 5,
            "devtools": 5,
            "customer_support": 4,
            "conversational_ai": 4,
            "contact_center": 4,
            "fintech": 4,
            "insurtech": 4,
            "cybersecurity": 4,
            "security": 4,
            "healthtech": 4,
            "saas": 3,
            "other": 1,
        },
    },
    "title_match": {
        "weight": 5,
        "description": "Contact title match to primary buyer persona",
        "scoring": {
            "cto": 5,
            "vp_engineering": 5,
            "svp_engineering": 5,
            "head_of_engineering": 3,
            "head_of_platform": 3,
            "director_engineering": 3,
            "principal_engineer": 2,
            "engineering_manager": 2,
            "other": 0,
        },
    },
}

TIERS = {
    "Hot": 75,
    "Warm": 50,
    "Cold": 0,
}

PRODUCT_CONTEXT = """
P95.AI is an AI performance optimization platform built for engineering teams running LLMs in production.

Core value props:
- Slashes p95/p99 inference latency and reduces tail latency spikes that break SLAs
- Cuts AI infrastructure costs without requiring model retraining
- Improves reliability with better visibility into inference bottlenecks and regressions
- Helps engineering leaders balance speed, quality, and cost across production AI systems

Ideal buyer pain: "We're running AI features in production, latency and reliability are inconsistent,
and our inference costs are climbing faster than our visibility into what is causing it."

The CTO / VP Engineering owns this problem. They feel it during incidents, margin reviews,
and every time a key AI feature slows down or becomes unpredictable.
"""

NEGATIVE_ICP = [
    "No AI-in-production signals and zero AI/platform hiring",
    "Pre-seed or sub-100-employee companies still in experimentation mode",
    "Services firms without a scaled software product surface",
    "Non-technical contacts outside engineering, ML, or infrastructure leadership",
]
