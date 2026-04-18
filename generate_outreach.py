"""
generate_outreach.py — CLI for generating personalized outreach via Claude API

Usage:
    python generate_outreach.py --input output/scored_leads.csv --output output/outreach.csv
    python generate_outreach.py --input output/scored_leads.csv --output output/outreach.csv --all
    python generate_outreach.py --input output/scored_leads.csv --output output/outreach.csv --top 20
"""

import argparse
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outreach.generator import generate_outreach_batch


def main():
    parser = argparse.ArgumentParser(
        description="Generate personalized outreach for scored leads using Claude API"
    )
    parser.add_argument(
        "--input",  required=True,
        help="Scored leads CSV (output of score_leads.py)"
    )
    parser.add_argument(
        "--output", required=True,
        help="Output CSV with outreach messages added"
    )
    parser.add_argument(
        "--top", type=int, default=None,
        help="Generate outreach for the top N leads by score (default: all rows in input)"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Generate outreach for all scored leads in the input CSV"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Seconds to wait between API calls (default: 1.0)"
    )
    args = parser.parse_args()

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n[ERROR] ANTHROPIC_API_KEY environment variable not set.")
        print("Add it to your .env file:\n  ANTHROPIC_API_KEY=sk-ant-...")
        print("Then run: source .env  (or use python-dotenv)")
        sys.exit(1)

    # Load scored leads
    print(f"Loading scored leads from {args.input}...")
    df = pd.read_csv(args.input)

    if "raw_score" not in df.columns:
        print("[ERROR] This CSV doesn't have a 'raw_score' column.")
        print("Run score_leads.py first to score your leads.")
        sys.exit(1)

    # Sort by score, take top N
    df_sorted = df.sort_values("raw_score", ascending=False).reset_index(drop=True)
    target_count = None if args.all or args.top is None else args.top
    leads = df_sorted.to_dict("records") if target_count is None else df_sorted.head(target_count).to_dict("records")

    if not leads:
        print("[ERROR] No leads found in input CSV.")
        sys.exit(1)

    scope = "all leads" if target_count is None else f"top {len(leads)} leads"
    print(f"Generating outreach for {scope}...")
    print(f"Score range: {leads[0]['raw_score']} (highest) → {leads[-1]['raw_score']} (lowest)")

    # Generate
    enriched = generate_outreach_batch(leads, top_n=target_count, delay_seconds=args.delay)

    # Mark A/B candidates (top 20 of the generated set)
    for i, lead in enumerate(enriched):
        lead["is_ab_candidate"] = "Yes" if i < 20 else "No"

    # Save
    out_df = pd.DataFrame(enriched)
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    out_df.to_csv(args.output, index=False)
    print(f"\nOutreach saved to {args.output}")

    # Summary
    generated = out_df[out_df["outreach_status"] == "generated"]
    failed    = out_df[out_df["outreach_status"] != "generated"]
    print(f"Generated: {len(generated)} | Failed: {len(failed)}")

    if not failed.empty:
        print("\nFailed leads:")
        for _, row in failed.iterrows():
            print(f"  {row.get('contact_name', '?')} @ {row.get('company_name', '?')}: {row['outreach_status']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
