"""
generator.py — Outreach generation using Claude API.
Generates cold email (A/B), LinkedIn DM (A/B), and a sendable outreach brief
for each lead.
"""

import copy
import os
import json
import time
import requests
from typing import Dict, List, Optional
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.icp_config import PRODUCT_CONTEXT

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL   = "claude-sonnet-4-20250514"


def _get_api_key() -> str:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Add it to your .env file or export it."
        )
    return key


def _call_claude(prompt: str, max_tokens: int = 1500) -> str:
    """Make a single call to Claude API and return text response."""
    headers = {
        "x-api-key": _get_api_key(),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["content"][0]["text"].strip()


def _build_prompt(lead: Dict) -> str:
    """Build the outreach generation prompt for a single lead."""
    return f"""You are an elite B2B cold outreach copywriter. Your emails get 30%+ reply rates from technical executives.

--- PRODUCT ---
{PRODUCT_CONTEXT}

--- LEAD PROFILE ---
Company: {lead.get('company_name', 'N/A')}
Domain: {lead.get('domain', 'N/A')}
Industry: {lead.get('industry', 'N/A')}
Headcount: {lead.get('headcount', 'N/A')}
Funding: {lead.get('funding_stage', 'N/A')} (funded {lead.get('funding_recency_months', '?')} months ago)
Tech stack: {lead.get('tech_stack', 'N/A')}
AI job postings (90d): {lead.get('ai_job_postings_90d', '0')}
Recent trigger: {lead.get('recent_trigger', 'None specified')}

Contact: {lead.get('contact_name', 'N/A')}, {lead.get('contact_title', 'N/A')}
ICP Score: {lead.get('tier', 'N/A')} ({lead.get('raw_score', 'N/A')}/100)
Why they scored high: {lead.get('score_explanation', 'N/A')}

--- TASK ---
Generate outreach in this exact format. Return ONLY valid JSON — no preamble, no markdown fences.

{{
  "email_a": {{
    "label": "COLD EMAIL (Version A — Pain-led hook)",
    "subject": "...",
    "body": "..."
  }},
  "email_b": {{
    "label": "COLD EMAIL (Version B — Curiosity/ROI hook)",
    "subject": "...",
    "body": "..."
  }},
  "linkedin_a": {{
    "label": "LINKEDIN DM (Version A — conversational, under 75 words)",
    "body": "..."
  }},
  "linkedin_b": {{
    "label": "LINKEDIN DM (Version B — slightly more direct, under 75 words)",
    "body": "..."
  }},
  "ab_hypothesis": {{
    "label": "A/B TEST HYPOTHESIS for this lead",
    "version_a_targets": "...",
    "version_b_targets": "...",
    "predicted_winner": "A or B",
    "reasoning": "...",
    "how_to_measure": "reply rate / positive reply rate / meeting booked"
  }}
}}

STRICT RULES:
- Every message MUST reference at least one specific verifiable signal from their company
- Emails: 3–4 sentences max. Subject line: under 8 words, no emojis
- LinkedIn DMs: under 75 words, conversational tone
- NEVER start with "I hope this finds you well" or any generic opener
- NEVER use the phrase "AI-powered" generically
- Email body must have: [1] specific company insight → [2] the pain it causes → [3] one-sentence P95.AI value prop → [4] low-friction CTA
- The two email variants must use DIFFERENT pain points or hooks
- Use the lead's exact company, contact, score, tech stack signals, and recent trigger when relevant
- Keep subjects under 8 words
- LinkedIn DMs must stay under 75 words
"""


def _build_sendable_format(lead: Dict) -> str:
    """Build a single outreach brief string the user can send or review."""
    return "\n".join([
        "COLD EMAIL (Version A — Pain-led hook)",
        f"Subject: {lead.get('email_a_subject', '')}",
        f"Body: {lead.get('email_a_body', '')}",
        "",
        "COLD EMAIL (Version B — Curiosity/ROI hook)",
        f"Subject: {lead.get('email_b_subject', '')}",
        f"Body: {lead.get('email_b_body', '')}",
        "",
        "LINKEDIN DM (Version A — conversational, under 75 words)",
        lead.get("linkedin_a", ""),
        "",
        "LINKEDIN DM (Version B — slightly more direct, under 75 words)",
        lead.get("linkedin_b", ""),
        "",
        "A/B TEST HYPOTHESIS for this lead",
        f"- Version A targets: {lead.get('ab_version_a_targets', '')}",
        f"- Version B targets: {lead.get('ab_version_b_targets', '')}",
        f"- Predicted winner: {lead.get('ab_predicted_winner', '')} because {lead.get('ab_reasoning', '')}",
        f"- How to measure: {lead.get('ab_how_to_measure', '')}",
    ])


def generate_outreach_for_lead(lead: Dict, retries: int = 2) -> Dict:
    """
    Generate all 4 outreach variants for a single lead.
    Returns the lead dict enriched with outreach fields.
    """
    prompt = _build_prompt(lead)

    for attempt in range(retries + 1):
        try:
            raw = _call_claude(prompt)

            # Strip any accidental markdown fences
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            parsed = json.loads(raw)

            enriched = copy.deepcopy(lead)
            enriched["email_a_subject"] = parsed["email_a"]["subject"]
            enriched["email_a_body"] = parsed["email_a"]["body"]
            enriched["email_b_subject"] = parsed["email_b"]["subject"]
            enriched["email_b_body"] = parsed["email_b"]["body"]
            enriched["linkedin_a"] = parsed["linkedin_a"]["body"]
            enriched["linkedin_b"] = parsed["linkedin_b"]["body"]
            enriched["ab_version_a_targets"] = parsed["ab_hypothesis"]["version_a_targets"]
            enriched["ab_version_b_targets"] = parsed["ab_hypothesis"]["version_b_targets"]
            enriched["ab_predicted_winner"] = parsed["ab_hypothesis"]["predicted_winner"]
            enriched["ab_reasoning"] = parsed["ab_hypothesis"]["reasoning"]
            enriched["ab_how_to_measure"] = parsed["ab_hypothesis"]["how_to_measure"]
            enriched["outreach_brief"] = _build_sendable_format(enriched)
            enriched["outreach_status"] = "generated"
            return enriched

        except (json.JSONDecodeError, KeyError) as e:
            if attempt < retries:
                time.sleep(2)
                continue
            failed = copy.deepcopy(lead)
            failed["outreach_status"] = f"failed: {str(e)}"
            failed["raw_claude_response"] = raw if 'raw' in locals() else ""
            failed["outreach_brief"] = ""
            return failed

        except requests.HTTPError as e:
            failed = copy.deepcopy(lead)
            failed["outreach_status"] = f"api_error: {str(e)}"
            failed["outreach_brief"] = ""
            return failed

    return lead


def generate_outreach_batch(
    leads: List[Dict],
    top_n: Optional[int] = 50,
    delay_seconds: float = 1.0,
) -> List[Dict]:
    """
    Generate outreach for the requested leads.
    Includes a small delay between calls to avoid rate limiting.

    Args:
        leads: list of lead dicts (already scored)
        top_n: how many leads to generate outreach for; None means all
        delay_seconds: pause between API calls

    Returns:
        enriched list of lead dicts
    """
    target = leads if top_n is None else leads[:top_n]
    results = []

    print(f"\nGenerating outreach for {len(target)} leads...")

    for i, lead in enumerate(target, 1):
        name    = lead.get("contact_name", "?")
        company = lead.get("company_name", "?")
        score   = lead.get("raw_score", "?")
        print(f"  [{i}/{len(target)}] {name} @ {company} (score: {score})")

        enriched = generate_outreach_for_lead(lead)
        results.append(enriched)

        if i < len(target):
            time.sleep(delay_seconds)

    success = sum(1 for r in results if r.get("outreach_status") == "generated")
    print(f"\nDone. {success}/{len(target)} outreach messages generated successfully.")

    return results
