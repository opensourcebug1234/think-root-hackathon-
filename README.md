# P95.AI Lead Scoring & Outreach Pipeline
### ThinkRoot × Vortex Hackathon 2026 — Track A

An end-to-end pipeline for intelligent lead qualification and personalized outreach targeting CTOs and VP Engineering at enterprise companies running AI in production.

---

## Results

| Metric | Value |
|---|---|
| Leads sourced | 200+ |
| Enrichment fields per lead | 13 |
| Scoring criteria | 10 weighted dimensions |
| Tier classification | Hot / Warm / Cold |
| Personalized outreach generated | Top N or all scored leads |
| A/B test variants | 2 per lead |

---

## Project Structure

```
lead-pipeline/
├── app/
│   ├── main.py            # FastAPI app for website + API
│   ├── static/            # frontend assets
│   └── templates/         # HTML templates
│
├── score_leads.py          # CLI: score all leads, output CSV
├── generate_outreach.py    # CLI: generate emails + DMs via Claude API
├── mock_leads.py           # generates sample data for testing
│
├── config/
│   └── icp_config.py       # ICP criteria, weights, tier thresholds — edit here
│
├── models/
│   └── scorer.py           # scoring logic with full explainability
│
├── outreach/
│   └── generator.py        # Claude API integration for outreach generation
│
├── data/
│   └── raw_leads.csv       # input: Clay export (or mock_leads.py output)
│
├── output/                 # all generated files land here (gitignored)
│
├── .env.example            # copy to .env and add your API key
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Clone and install

```bash
git clone https://github.com/your-team/lead-pipeline
cd lead-pipeline
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-your-key-here
export $(cat .env | xargs)
```

### 3. Get your leads (two options)

**Option A — Real leads from Clay.com**
1. Go to [clay.com](https://clay.com) and create a table
2. Import from Apollo.io / LinkedIn / BuiltWith using Clay integrations
3. Export as CSV with the required column names (see below)

**Option B — Mock data for testing**
```bash
python mock_leads.py --count 220 --output data/raw_leads.csv
```

### 4. Run the website locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open `http://localhost:8000`.

The web app includes:
- mock lead generation
- CSV upload + scoring
- outreach generation with downloadable `outreach_brief` blocks
- REST endpoints for health, scoring, and outreach

### 5. Score all leads from the CLI

```bash
python score_leads.py \
  --input data/raw_leads.csv \
  --output output/scored_leads.csv \
  --report \
  --top 50
```

Output files:
- `output/scored_leads.csv` — all leads with score, tier, explanation
- `output/scored_leads_top50.csv` — top 50 leads only

### 6. Generate personalized outreach from the CLI

```bash
python generate_outreach.py \
  --input output/scored_leads.csv \
  --output output/outreach.csv \
  --all
```

Output: `output/outreach.csv` with 4 outreach variants per lead:
- `email_a_subject` / `email_a_body` — pain-led hook
- `email_b_subject` / `email_b_body` — ROI-led hook
- `linkedin_a` — conversational DM
- `linkedin_b` — direct DM
- `ab_predicted_winner` + `ab_reasoning` — A/B hypothesis
- `outreach_brief` — one sendable block in the target format for each company

Use `--top 50` if you only want outreach for a ranked subset instead of every target in the file.

### 7. API endpoints

The website exposes a deployment-friendly API:

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | `GET` | Healthcheck for deployment and uptime monitoring |
| `/api/mock-leads` | `POST` | Generate mock lead CSV payloads |
| `/api/score` | `POST` | Score uploaded Clay CSVs |
| `/api/outreach` | `POST` | Generate outreach for scored leads |

### 8. ThinkRoot deployment shape

ThinkRoot appears to support hosted apps and APIs. This project is now packaged as a standard Python ASGI web app, so the deployment target should point to:

```text
app.main:app
```

If ThinkRoot asks for a start command, use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Required environment variables:

```text
ANTHROPIC_API_KEY=...
```

---

## CSV Schema

Your input CSV must have these columns:

| Column | Type | Example | Source |
|---|---|---|---|
| `company_name` | string | "Acme AI" | Clay / Apollo |
| `domain` | string | "acme.ai" | Clay |
| `headcount` | int | 350 | Clay / LinkedIn |
| `funding_stage` | string | "Series B" | Crunchbase |
| `funding_recency_months` | int | 4 | Crunchbase |
| `tech_stack` | string (comma-sep) | "openai,pytorch,aws" | BuiltWith / Clay |
| `ai_job_postings_90d` | int | 8 | LinkedIn Jobs / Clay |
| `contact_name` | string | "Jane Smith" | Apollo / LinkedIn |
| `contact_title` | string | "VP Engineering" | LinkedIn |
| `contact_email` | string | "jane@acme.ai" | Apollo / Clay |
| `contact_linkedin` | string | "linkedin.com/in/..." | LinkedIn |
| `industry` | string | "SaaS" | Apollo / manual |
| `recent_trigger` | string | "Raised Series B 3mo ago" | Manual / Clay AI |

Optional columns used when available:

| Column | Type | Example | Source |
|---|---|---|---|
| `arr_millions` | float | 85 | Crunchbase / manual |
| `arr` | string or number | "$85M" | Manual / web research |
| `annual_revenue` | string or number | "$85M-$100M" | Manual / enrichment |
| `annual_revenue_usd` | int | 85000000 | Manual / enrichment |
| `revenue` | string or number | "85M" | Manual / enrichment |

---

## Lead Scoring Model

Each lead is scored `0–100` across `10 weighted dimensions`. The model is deterministic, explainable, and implemented in [config/icp_config.py](/Users/animeshjha/Downloads/lead-pipeline/config/icp_config.py:1) and [models/scorer.py](/Users/animeshjha/Downloads/lead-pipeline/models/scorer.py:1).

| Criterion | Weight | What we measure |
|---|---|---|
| AI-in-production evidence | 20 | Managed model platforms, LLM frameworks, or public production AI signals |
| Inference scale and complexity | 15 | Evidence of multi-model, self-hosted, GPU, Kubernetes, routing, or latency-sensitive AI workloads |
| AI observability and reliability maturity | 10 | Signals like LangSmith, Datadog, OpenTelemetry, MLflow, or reliability-related trigger terms |
| AI job postings (90d) | 10 | Hiring intensity for AI, ML platform, inference, or MLOps roles |
| Headcount fit | 10 | Enterprise sweet spot centered on 200–3,000 employees |
| ARR / monetization pressure | 10 | ARR fields when available, otherwise launch or commercial trigger proxies |
| Funding stage | 8 | Series A-C and growth-stage companies score highest |
| Business urgency | 7 | Recent funding or trigger events like launch, incident, or rapid hiring |
| Industry fit | 5 | AI/ML, DevTools, Fintech, Security, Healthtech, and adjacent high-fit categories |
| Buyer title match | 5 | CTO, VP Engineering, SVP Engineering, Head of Engineering, or Head of Platform |

Weights sum to `100`.

**Tiers:**
- **Hot** — 75+ — immediate outreach priority
- **Warm** — 50–74 — nurture sequence
- **Cold** — <50 — deprioritize

**Every lead has a human-readable explanation** listing the top 3 scoring factors, for example:
> `Hot (82/100): AI in production: aws bedrock, langchain, openai (+20pts) | Inference complexity: kubernetes, latency, gpu (+15pts) | 7 AI/platform job postings (90d) (+10pts)`

### How To Update Weights For Future Campaigns

Edit [config/icp_config.py](/Users/animeshjha/Downloads/lead-pipeline/config/icp_config.py:1). Each criterion has:

- a `weight`
- one or more scoring buckets or signal lists
- tier thresholds in `TIERS`

When changing weights:

1. Make sure all `weight` values still sum to `100`
2. Keep the corresponding scoring function in [models/scorer.py](/Users/animeshjha/Downloads/lead-pipeline/models/scorer.py:1) aligned with the config buckets
3. Re-run scoring on a small known-good / known-bad sample before changing production outreach priorities

### How To Validate The Model Against Known Good / Bad Leads

Create a small benchmark CSV with:

- `10-20` leads you believe should be `Hot`
- `10-20` leads you believe should be `Cold`
- a few borderline `Warm` examples

Then:

1. Run `python3 score_leads.py --input benchmark.csv --output benchmark_scored.csv --report`
2. Check whether known strong leads land in `Hot` and weak leads land in `Cold`
3. Review each lead’s `score_explanation` to see whether the top factors match human judgment
4. If the ranking feels wrong, update the weights or scoring buckets in `config/icp_config.py`
5. Repeat until the model cleanly separates obviously good and obviously bad leads

### Explainability Report

Use the CLI with `--report` to print a console summary. For each hot lead, the script prints:

```text
Why this lead scored X: [factor1 +W pts], [factor2 +W pts], [factor3 +W pts]
```

---

## Outreach Generation

The pipeline calls the Claude API once per lead and generates:
1. Cold email Version A — pain-led hook (latency/reliability problem)
2. Cold email Version B — ROI-led hook (cost/efficiency angle)
3. LinkedIn DM Version A — conversational, under 75 words
4. LinkedIn DM Version B — direct, slightly more assertive

Each generation also includes an **A/B test hypothesis** with predicted winner and reasoning.

**Rate limiting:** The generator adds a 1-second delay between calls by default. Use `--delay 2` if you hit rate limits.

---

## Reproducing This Pipeline

To re-run with fresh data next month:

1. Export a new CSV from Clay (same column schema)
2. Run `score_leads.py` with the new file
3. Run `generate_outreach.py` on the new top 50
4. All outputs are deterministic given the same input + ICP config

Total runtime on 200 leads: ~3 minutes for scoring, ~10 minutes for outreach generation (API calls).

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Clay.com | Lead enrichment and data aggregation |
| Apollo.io | Contact + company data sourcing |
| LinkedIn Sales Nav | Seniority and title verification |
| BuiltWith | Tech stack detection |
| Crunchbase | Funding stage and recency |
| Python + pandas | Scoring model and data pipeline |
| Anthropic Claude API | Personalized outreach generation |
| GitHub | Version control and reproducibility |
| ThinkRoot.dev | Project documentation site |
# think-root-hackathon-
# think-root-hackathon-
