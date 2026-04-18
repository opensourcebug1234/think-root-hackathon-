"""
score_leads.py — CLI entry point for lead scoring

Usage:
    python score_leads.py --input leads.csv --output scored_leads.csv
    python score_leads.py --input leads.csv --output scored_leads.csv --report
"""

import argparse
import os
import sys
from typing import List

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.scorer import score_dataframe, get_top_leads


REQUIRED_COLUMNS = [
    "company_name",
    "domain",
    "headcount",
    "funding_stage",
    "funding_recency_months",
    "tech_stack",
    "ai_job_postings_90d",
    "contact_name",
    "contact_title",
    "contact_email",
    "industry",
]

OPTIONAL_COLUMNS = [
    "contact_linkedin",
    "recent_trigger",
    "arr_millions",
    "arr",
    "annual_revenue",
    "annual_revenue_usd",
    "revenue",
]


def validate_columns(df: pd.DataFrame) -> None:
    """
    Validate that the CSV contains the minimum required scoring columns.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print(f"\n[ERROR] Missing required columns: {missing}")
        print(f"Your CSV has: {list(df.columns)}")
        print(f"\nRequired columns: {REQUIRED_COLUMNS}")
        print(f"Optional columns: {OPTIONAL_COLUMNS}")
        sys.exit(1)


def _extract_top_factors(explanation: str) -> List[str]:
    """
    Extract factor strings from the human-readable explanation.
    """
    if ": " not in explanation:
        return []
    _, factors = explanation.split(": ", 1)
    if factors == "No qualifying ICP signals":
        return [factors]
    return factors.split(" | ")


def print_report(df: pd.DataFrame) -> None:
    """
    Print a simple explainability report for the scored DataFrame.
    """
    print("\n" + "="*60)
    print("LEAD SCORING REPORT")
    print("="*60)
    print(f"\nTotal leads scored: {len(df)}")

    tier_counts = df["tier"].value_counts()
    for tier in ["Hot", "Warm", "Cold"]:
        count = tier_counts.get(tier, 0)
        pct   = round(count / len(df) * 100)
        bar   = "█" * (count // max(1, len(df) // 20))
        print(f"  {tier:<6}: {count:>4} ({pct:>2}%)  {bar}")

    print(f"\nAverage score : {df['raw_score'].mean():.1f}")
    print(f"Median score  : {df['raw_score'].median():.1f}")
    print(f"Max score     : {df['raw_score'].max()}")
    print(f"Min score     : {df['raw_score'].min()}")

    hot = df[df["tier"] == "Hot"].sort_values("raw_score", ascending=False)
    if not hot.empty:
        print(f"\nHOT LEAD EXPLAINABILITY:")
        print("-"*60)
        for _, row in hot.iterrows():
            factors = ", ".join(_extract_top_factors(row["score_explanation"]))
            print(f"Why this lead scored {row['raw_score']}: {factors}")
            print(f"  {row['contact_name']} @ {row['company_name']}")
            print()


def main():
    """
    Parse CLI arguments, score the input CSV, and write the results.
    """
    parser = argparse.ArgumentParser(
        description="Score B2B leads against the P95.AI ICP"
    )
    parser.add_argument(
        "--input",  required=True,
        help="Path to raw leads CSV (from Clay export or mock_leads.py)"
    )
    parser.add_argument(
        "--output", required=True,
        help="Path to write scored leads CSV"
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Print a scoring summary report to console"
    )
    parser.add_argument(
        "--top", type=int, default=50,
        help="Also export a separate CSV of top N leads (default: 50)"
    )
    args = parser.parse_args()

    # Load
    print(f"Loading leads from {args.input}...")
    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} leads.")

    # Validate
    validate_columns(df)

    # Score
    print("Scoring leads...")
    scored = score_dataframe(df)
    scored_sorted = scored.sort_values("raw_score", ascending=False).reset_index(drop=True)

    # Save full output
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    scored_sorted.to_csv(args.output, index=False)
    print(f"Scored leads saved to {args.output}")

    # Save top N separately
    top_path = args.output.replace(".csv", f"_top{args.top}.csv")
    get_top_leads(scored_sorted, n=args.top).to_csv(top_path, index=False)
    print(f"Top {args.top} leads saved to {top_path}")

    # Optional report
    if args.report:
        print_report(scored_sorted)

    print("\nDone.")


if __name__ == "__main__":
    main()
