"""
scorer.py — Lead scoring logic for P95.AI ICP
Each function returns (points_awarded: int, label: str) for explainability.
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.icp_config import ICP_CRITERIA, TIERS


# =============================================================================
# Helpers
# =============================================================================

ARR_FIELD_CANDIDATES = [
    "arr_millions",
    "arr",
    "annual_revenue",
    "annual_revenue_usd",
    "revenue",
]


def _safe_int(val, default: int = 0) -> int:
    try:
        return int(val) if not pd.isna(val) else default
    except (ValueError, TypeError):
        return default


def _normalize_text(raw) -> str:
    if pd.isna(raw) or raw is None:
        return ""
    return str(raw).strip().lower()


def _normalize_tech_stack(raw: str) -> List[str]:
    if pd.isna(raw) or not raw:
        return []
    return [t.strip().lower() for t in str(raw).split(",") if t.strip()]


def _contains_signal(text: str, signal: str) -> bool:
    return signal in text


def _find_matches(text: str, signals: List[str]) -> List[str]:
    return [signal for signal in signals if _contains_signal(text, signal)]


def _dedupe_keep_order(values: List[str]) -> List[str]:
    seen = set()
    ordered = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def _trigger_bucket(text: str, keyword_map: Dict[str, int]) -> Tuple[int, str]:
    bucket_keywords = {
        "incident": ["incident", "outage", "downtime", "latency issue", "sla", "degraded", "cost spike"],
        "launch": ["launch", "launched", "general availability", "ga", "ai product", "copilot", "assistant", "rag"],
        "hiring": ["hiring", "roles", "job postings", "ml engineer", "inference engineer", "platform engineer"],
        "leadership": ["cto joined", "vp engineering joined", "joined from", "new cto", "new vp"],
        "growth": ["expanded", "grew", "scale-up", "scaled", "employees in 6 months"],
        "monetization": ["pricing", "premium", "paid", "monetization", "upsell"],
        "margin": ["margin", "unit economics", "efficiency", "finops", "cost"],
        "enterprise": ["enterprise", "sso", "soc 2", "compliance", "security review"],
    }

    best_score = 0
    best_label = ""
    for bucket, score in keyword_map.items():
        keywords = bucket_keywords.get(bucket, [])
        if any(keyword in text for keyword in keywords) and score > best_score:
            best_score = score
            best_label = bucket
    return best_score, best_label


def _parse_arr_millions(row: pd.Series) -> Optional[float]:
    for field in ARR_FIELD_CANDIDATES:
        raw = row.get(field)
        if raw is None or pd.isna(raw):
            continue

        if isinstance(raw, (int, float)):
            if field == "arr_millions":
                return float(raw)
            if raw >= 1_000_000:
                return float(raw) / 1_000_000
            return float(raw)

        text = _normalize_text(raw)
        if not text:
            continue

        range_match = re.search(
            r"(\d+(?:\.\d+)?)\s*([mb])?\s*(?:-|–|to)\s*(\d+(?:\.\d+)?)\s*([mb])?",
            text,
        )
        if range_match:
            low = float(range_match.group(1))
            low_unit = range_match.group(2) or range_match.group(4) or "m"
            return low * 1000 if low_unit == "b" else low

        amount_match = re.search(r"(\d+(?:\.\d+)?)\s*([mb])", text)
        if amount_match:
            amount = float(amount_match.group(1))
            unit = amount_match.group(2)
            return amount * 1000 if unit == "b" else amount

        plain_number = re.search(r"\d+(?:\.\d+)?", text)
        if plain_number:
            amount = float(plain_number.group(0))
            if field == "arr_millions":
                return amount
            if amount >= 1_000_000:
                return amount / 1_000_000
            return amount

    return None


def _normalize_title(title: str) -> str:
    t = _normalize_text(title).replace("-", " ").replace("_", " ")
    if not t:
        return "other"

    if any(k in t for k in ["cto", "chief technology", "chief technical"]):
        return "cto"
    if any(k in t for k in ["svp engineering", "senior vice president engineering"]):
        return "svp_engineering"
    if any(
        k in t
        for k in [
            "vp engineering",
            "vp of engineering",
            "vice president engineering",
            "vice president of engineering",
        ]
    ):
        return "vp_engineering"
    if any(k in t for k in ["head of platform", "head of infrastructure", "head of ml platform"]):
        return "head_of_platform"
    if any(k in t for k in ["head of engineering", "head of technology"]):
        return "head_of_engineering"
    if any(k in t for k in ["director of engineering", "director engineering", "engineering director"]):
        return "director_engineering"
    if any(k in t for k in ["principal engineer", "staff engineer", "principal software engineer"]):
        return "principal_engineer"
    if any(k in t for k in ["engineering manager", "manager of engineering"]):
        return "engineering_manager"
    return "other"


def _normalize_industry(industry: str) -> str:
    i = _normalize_text(industry)
    if not i:
        return "other"

    ordered_matches = [
        ("customer_support", ["customer support", "support automation"]),
        ("conversational_ai", ["conversational ai", "voice ai", "chatbot"]),
        ("contact_center", ["contact center", "call center"]),
        ("cybersecurity", ["cybersecurity"]),
        ("security", ["security"]),
        ("insurtech", ["insurtech", "insurance"]),
        ("fintech", ["fintech", "payments"]),
        ("healthtech", ["healthtech", "clinical", "health"]),
        ("devtools", ["devtools", "developer tools", "developer platform"]),
        ("ai", ["ai/ml", "artificial intelligence", " ai"]),
        ("ml", ["machine learning"]),
        ("saas", ["saas"]),
    ]
    for label, patterns in ordered_matches:
        if any(pattern in i for pattern in patterns):
            return label
    return "other"


# =============================================================================
# Scoring functions
# =============================================================================

def score_ai_in_production(tech_stack_raw: str, recent_trigger_raw: str) -> Tuple[int, str]:
    config = ICP_CRITERIA["ai_in_production"]
    tech_text = " ".join(_normalize_tech_stack(tech_stack_raw))
    trigger_text = _normalize_text(recent_trigger_raw)

    platform_matches = _find_matches(tech_text, config["managed_platform_signals"])
    framework_matches = _find_matches(tech_text, config["framework_signals"])
    keyword_matches = _find_matches(trigger_text, config["production_keywords"])
    all_matches = _dedupe_keep_order(platform_matches + framework_matches + keyword_matches)

    if (len(platform_matches) >= 2 and len(framework_matches) >= 1) or len(all_matches) >= 4:
        return 20, f"AI in production: {', '.join(all_matches[:4])}"
    if len(platform_matches) >= 1 and (len(framework_matches) >= 1 or len(keyword_matches) >= 1):
        return 12, f"Production AI signals: {', '.join(all_matches[:3])}"
    if all_matches:
        return 6, f"Partial AI signal: {', '.join(all_matches[:2])}"
    return 0, "No clear AI-in-production evidence"


def score_inference_complexity(tech_stack_raw: str, recent_trigger_raw: str) -> Tuple[int, str]:
    config = ICP_CRITERIA["inference_scale_complexity"]
    tech_text = " ".join(_normalize_tech_stack(tech_stack_raw))
    trigger_text = _normalize_text(recent_trigger_raw)

    serving_matches = _find_matches(tech_text, config["serving_signals"])
    keyword_matches = _find_matches(trigger_text, config["complexity_keywords"])
    all_matches = _dedupe_keep_order(serving_matches + keyword_matches)

    if len(serving_matches) >= 2 or len(all_matches) >= 3:
        return 15, f"Inference complexity: {', '.join(all_matches[:3])}"
    if len(all_matches) >= 2:
        return 10, f"Scaled inference signal: {', '.join(all_matches[:2])}"
    if all_matches:
        return 5, f"Some inference complexity: {all_matches[0]}"
    return 0, "No strong inference-scale signal"


def score_observability_maturity(tech_stack_raw: str, recent_trigger_raw: str) -> Tuple[int, str]:
    config = ICP_CRITERIA["ai_observability_maturity"]
    tech_text = " ".join(_normalize_tech_stack(tech_stack_raw))
    trigger_text = _normalize_text(recent_trigger_raw)

    signal_matches = _find_matches(tech_text, config["signals"])
    keyword_matches = _find_matches(trigger_text, config["keywords"])
    all_matches = _dedupe_keep_order(signal_matches + keyword_matches)

    if len(signal_matches) >= 2 or (signal_matches and keyword_matches):
        return 10, f"AI observability maturity: {', '.join(all_matches[:3])}"
    if signal_matches or len(keyword_matches) >= 2:
        return 6, f"Reliability signal: {', '.join(all_matches[:2])}"
    if keyword_matches:
        return 3, f"Early observability clue: {keyword_matches[0]}"
    return 0, "No AI observability signal"


def score_job_postings(count_raw) -> Tuple[int, str]:
    n = _safe_int(count_raw)
    if n >= 5:
        return 10, f"{n} AI/platform job postings (90d)"
    if n >= 3:
        return 8, f"{n} AI/platform job postings (90d)"
    if n >= 1:
        return 5, f"{n} AI/platform job postings (90d)"
    return 0, "No AI/platform hiring signal"


def score_headcount(headcount_raw) -> Tuple[int, str]:
    n = _safe_int(headcount_raw)
    scoring = ICP_CRITERIA["headcount_fit"]["scoring"]

    if 400 <= n <= 2000:
        return scoring["400_2000"], f"{n} employees (best-fit scale)"
    if 200 <= n <= 399:
        return scoring["200_399"], f"{n} employees (core ICP)"
    if 2001 <= n <= 3000:
        return scoring["2001_3000"], f"{n} employees (strategic fit)"
    if 3001 <= n <= 10000:
        return scoring["3001_10000"], f"{n} employees (large enterprise)"
    if 100 <= n <= 199:
        return scoring["100_199"], f"{n} employees (emerging fit)"
    if n > 10000:
        return scoring["10001_plus"], f"{n} employees (very large enterprise)"
    return scoring["0_99"], f"{n} employees (below ICP floor)"


def score_arr_and_monetization(row: pd.Series) -> Tuple[int, str]:
    config = ICP_CRITERIA["arr_monetization_pressure"]
    arr_millions = _parse_arr_millions(row)
    recent_trigger = _normalize_text(row.get("recent_trigger", ""))
    headcount = _safe_int(row.get("headcount", 0))
    tech_signals = len(_normalize_tech_stack(row.get("tech_stack", "")))

    if arr_millions is not None:
        scoring = config["scoring_millions"]
        if 50 <= arr_millions <= 250:
            return scoring["50_250"], f"ARR signal: ~${arr_millions:.0f}M"
        if 20 <= arr_millions < 50:
            return scoring["20_49"], f"ARR signal: ~${arr_millions:.0f}M"
        if 250 < arr_millions <= 500:
            return scoring["251_500"], f"ARR signal: ~${arr_millions:.0f}M"
        if arr_millions > 500:
            return scoring["500_plus"], f"ARR signal: ~${arr_millions:.0f}M"
        if 10 <= arr_millions < 20:
            return scoring["10_19"], f"ARR signal: ~${arr_millions:.0f}M"
        return scoring["0_9"], f"ARR signal: ~${arr_millions:.0f}M"

    launch_keywords = ["launched", "launch", "ga", "general availability", "ai product", "copilot", "assistant"]
    monetization_keywords = ["pricing", "premium", "upsell", "enterprise", "margin", "unit economics"]

    if any(keyword in recent_trigger for keyword in launch_keywords):
        return config["trigger_keywords"]["launch"], "AI feature launch signal"
    if any(keyword in recent_trigger for keyword in monetization_keywords):
        return config["trigger_keywords"]["monetization"], "Commercial / margin signal"
    if headcount >= 400 and tech_signals >= 3:
        return config["trigger_keywords"]["proxy"], "Revenue-scale proxy from company size + AI stack"
    return 0, "No ARR or monetization signal"


def score_funding_stage(stage_raw: str) -> Tuple[int, str]:
    stage_scores = ICP_CRITERIA["funding_stage"]["scoring"]
    stage_label = _normalize_text(stage_raw).replace(" ", "_").replace("-", "_")
    if not stage_label:
        stage_label = "unknown"

    for key, score in stage_scores.items():
        if key != "unknown" and key in stage_label:
            display = str(stage_raw) if not pd.isna(stage_raw) else "unknown"
            return score, f"Funding stage: {display}"

    display = str(stage_raw) if not pd.isna(stage_raw) else "unknown"
    return stage_scores["unknown"], f"Funding stage: {display}"


def score_business_urgency(recency_months_raw, recent_trigger_raw: str) -> Tuple[int, str]:
    config = ICP_CRITERIA["business_urgency"]
    months = _safe_int(recency_months_raw, default=99)
    trigger_text = _normalize_text(recent_trigger_raw)

    recency_scores = config["recency_scoring"]
    if months <= 9:
        recency_pts = recency_scores["0_9"]
    elif months <= 18:
        recency_pts = recency_scores["10_18"]
    elif months <= 30:
        recency_pts = recency_scores["19_30"]
    else:
        recency_pts = recency_scores["31_plus"]

    trigger_pts, trigger_bucket = _trigger_bucket(trigger_text, config["trigger_keywords"])
    if trigger_pts >= recency_pts and trigger_bucket:
        return trigger_pts, f"Urgency trigger: {trigger_bucket}"
    if recency_pts > 0:
        return recency_pts, f"Recent funding: {months}mo ago"
    if trigger_pts > 0:
        return trigger_pts, f"Urgency trigger: {trigger_bucket}"
    return 0, "No urgency signal"


def score_industry(industry_raw: str) -> Tuple[int, str]:
    normalized = _normalize_industry(industry_raw)
    pts = ICP_CRITERIA["industry_fit"]["scoring"].get(normalized, 1)
    display = str(industry_raw) if not pd.isna(industry_raw) else "unknown"
    return pts, f"Industry: {display}"


def score_title(title_raw: str) -> Tuple[int, str]:
    normalized = _normalize_title(title_raw)
    pts = ICP_CRITERIA["title_match"]["scoring"].get(normalized, 0)
    display = str(title_raw) if not pd.isna(title_raw) else "unknown"
    return pts, f"Title: {display}"


# =============================================================================
# Main scoring entry point
# =============================================================================

def score_lead(row: pd.Series) -> Dict[str, Any]:
    """
    Score a single lead row from the CSV.

    Returns:
        A dictionary with:
        - raw_score: integer score from 0-100
        - tier: Hot / Warm / Cold
        - score_explanation: human-readable explanation of the top 3 factors
        - score_breakdown: full internal breakdown for debugging or future use
    """
    results = [
        score_ai_in_production(row.get("tech_stack", ""), row.get("recent_trigger", "")),
        score_inference_complexity(row.get("tech_stack", ""), row.get("recent_trigger", "")),
        score_observability_maturity(row.get("tech_stack", ""), row.get("recent_trigger", "")),
        score_job_postings(row.get("ai_job_postings_90d", 0)),
        score_headcount(row.get("headcount", 0)),
        score_arr_and_monetization(row),
        score_funding_stage(row.get("funding_stage", "unknown")),
        score_business_urgency(row.get("funding_recency_months", 99), row.get("recent_trigger", "")),
        score_industry(row.get("industry", "")),
        score_title(row.get("contact_title", "")),
    ]

    total = min(sum(points for points, _ in results), 100)

    if total >= TIERS["Hot"]:
        tier = "Hot"
    elif total >= TIERS["Warm"]:
        tier = "Warm"
    else:
        tier = "Cold"

    top3 = sorted(results, key=lambda item: item[0], reverse=True)[:3]
    explanation_parts = [f"{label} (+{points}pts)" for points, label in top3 if points > 0]
    if explanation_parts:
        explanation = f"{tier} ({total}/100): " + " | ".join(explanation_parts)
    else:
        explanation = f"{tier} ({total}/100): No qualifying ICP signals"
    breakdown = {label: points for points, label in results}

    return {
        "raw_score": total,
        "tier": tier,
        "score_explanation": explanation,
        "score_breakdown": str(breakdown),
    }


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Score all leads in a DataFrame.

    Returns the original DataFrame with exactly 3 scoring columns added:
    `raw_score`, `tier`, and `score_explanation`.
    """
    scores = df.apply(score_lead, axis=1, result_type="expand")
    return pd.concat([df, scores[["raw_score", "tier", "score_explanation"]]], axis=1)


def get_top_leads(df: pd.DataFrame, n: int = 50) -> pd.DataFrame:
    """Return top N leads sorted by score descending."""
    if "raw_score" not in df.columns:
        raise ValueError("Run score_dataframe() before get_top_leads()")
    return df.sort_values("raw_score", ascending=False).head(n).reset_index(drop=True)
