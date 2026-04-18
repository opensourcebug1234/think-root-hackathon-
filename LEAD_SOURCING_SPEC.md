# P95.AI Lead Sourcing Technical Spec

This document defines a reproducible sourcing workflow for generating `200+` enterprise engineering leads for P95.AI using `Clay`, `Apollo`, `LinkedIn Sales Navigator`, `BuiltWith`, `GitHub Search`, and `Crunchbase`.

It is designed to support the ICP in [ICP.md](/Users/animeshjha/Downloads/lead-pipeline/ICP.md:1), with a focus on:

- Companies with `200-3,000` employees
- High-fit verticals: AI-native SaaS, developer tooling, customer support / conversational AI, fintech, cybersecurity, and healthtech
- Production AI signals: `AWS Bedrock`, `Vertex AI`, `Azure OpenAI`, `vLLM`, `Triton`, `Ray`, `LangChain`, `MLflow`, `OpenTelemetry`, `Datadog LLM Observability`, `LangSmith`
- Buyer personas: `CTO`, `VP Engineering`, `SVP Engineering`, `Head of Engineering`, `Head of Platform`, `Head of Infrastructure`

## 1. PLATFORM STRATEGY

### Target Output Mix

| Platform | Primary Use | Raw Candidate Output | Expected Retained Records After Dedupe / QA | Notes |
|---|---|---:|---:|---|
| Apollo.io | Core account + contact sourcing | 120-180 contacts | 80-120 | Best source for structured company + people data |
| LinkedIn Sales Navigator | Title validation + account confirmation | 80-140 contacts | 50-90 | Highest contact-title quality, slower export motion |
| BuiltWith | Tech-signal account discovery | 60-100 accounts | 25-45 | Useful for stack proxies, weaker for backend-only AI tools |
| GitHub Search | Technical-fit account discovery and validation | 30-60 accounts | 15-30 | Highest technical precision, lower volume, more manual |
| Crunchbase | Funding and growth trigger discovery | 60-100 accounts | 25-45 | Best for recency, stage, and urgency signals |

**Expected final master table**

- `220-320` raw contacts before dedupe
- `200-240` validated contacts after dedupe and QA
- `120-170` unique accounts represented

### Apollo.io

**Why Apollo leads the workflow**

- Best structured blend of `company`, `contact`, `technologies`, and `job postings`
- Fastest way to source exportable records at scale
- Strongest seed source for Clay enrichment

**Apollo company search filters**

Use `Companies` search first, save results to a list, then run `People` search on only those saved accounts.

**Core company filter set**

```text
# of employees:
200-3000

Industry / market segments:
SaaS
Fintech
Developer Tools
Security
Healthtech

Funding:
Stage = Series A, Series B, Series C, Series D, Growth
Last funding date = last 18 months

Technologies:
OpenAI
Anthropic
AWS Bedrock
Vertex AI
Azure OpenAI
LangChain
LlamaIndex
MLflow
Ray
vLLM
Triton
Datadog
OpenTelemetry

Job postings:
"Machine Learning Engineer"
"ML Platform Engineer"
"AI Platform Engineer"
"Inference Engineer"
"MLOps Engineer"
"Platform Engineer"
Posted within last 90 days

Exclude industries / segments:
Consulting
Agencies
Staffing
Retail
Construction
Hospitality
```

**Apollo people search filters**

After saving accounts from the company search, switch to `People` search and filter to only those accounts.

```text
Saved account list:
P95 ICP - Apollo Accounts - YYYY-MM

Job title boolean:
("CTO" OR "Chief Technology Officer" OR "VP Engineering" OR "Vice President Engineering" OR
"SVP Engineering" OR "Senior Vice President Engineering" OR "Head of Engineering" OR
"Head of Platform" OR "Head of Infrastructure" OR "VP Platform Engineering")
NOT ("Interim" OR "Fractional" OR "Advisor" OR "Consultant" OR "Recruiter")

Management level:
C-Level
VP
Head
Director

Departments / functions:
Engineering
Information Technology
Infrastructure
Platform

Time in current role:
>= 6 months
```

**Expected lead volume**

- `50-80` accounts from company search
- `80-120` contacts from people search

**Quality vs. quantity**

- Highest quantity of structured exportable records
- Good technology + job posting coverage
- Slightly noisier titles than Sales Nav, so always validate top-tier leads there

### LinkedIn Sales Navigator

**Why use it**

- Best source for `title accuracy`, `seniority`, and `company/lead validation`
- Best second-pass validator after Apollo
- Useful for surfacing accounts Apollo missed

**Account search filters**

Create separate saved searches by vertical instead of one broad search.

**Saved search 1: AI / DevTools**

```text
Account filters

Geography:
United States
Canada
United Kingdom
Ireland
Netherlands
Germany
Israel

Industry:
Software Development
Technology, Information and Internet
Computer and Network Security

Company headcount:
201-500
501-1000
1001-5000

Keywords:
("AI" OR "LLM" OR "copilot" OR "assistant" OR "agent" OR "RAG" OR "model" OR "inference" OR "platform")
```

**Saved search 2: Fintech / Cyber / Healthtech**

```text
Account filters

Geography:
United States
Canada
United Kingdom

Industry:
Financial Services
Banking
Insurance
Computer and Network Security
Hospitals and Health Care
Health, Wellness and Fitness

Company headcount:
201-500
501-1000
1001-5000

Keywords:
("AI" OR "copilot" OR "automation" OR "assistant" OR "platform" OR "risk" OR "security" OR "clinical")
```

**Lead search filters**

Run lead search against saved accounts.

```text
Lead filters

Current job title:
CTO
Chief Technology Officer
VP Engineering
Vice President Engineering
SVP Engineering
Head of Engineering
Head of Platform
Head of Infrastructure

Seniority level:
CXO
VP
Director

Function:
Engineering
Information Technology

Spot-check keywords:
("AI" OR "platform" OR "infrastructure" OR "ML" OR "data" OR "reliability")
```

**Expected lead volume**

- `40-70` validated contacts
- `20-40` net new contacts not already found in Apollo

**Quality vs. quantity**

- Highest quality for role validation
- Lower throughput than Apollo
- Best used as a validator and fill-in source, not the sole export engine

### BuiltWith

**Why use it**

- Best for finding `technically mature` web properties
- Good for `tech-spend`, `employee`, `location`, and stack-proxy filtering
- Useful for sourcing accounts that are likely to have observability or platform sophistication

**BuiltWith search strategy**

BuiltWith is strongest on `website-detectable` technologies and commercial web patterns. It is weaker for backend-only inference infrastructure. Use it for discovery, then validate AI stack elsewhere.

**Search set A: platform maturity proxies**

```text
Technologies:
Datadog
New Relic
Segment
Cloudflare
Snowflake
Vercel

Filters:
Country = US, CA, GB, IE, NL, DE, IL
Employees >= 200
Tech spend >= $1000+
B2B / enterprise-oriented pages preferred
```

**Search set B: AI homepage keyword discovery**

```text
Website keyword lists:
"AI"
"LLM"
"copilot"
"RAG"
"agent"
"developer platform"
"security"

Filters:
Employees >= 200
Country = US, CA, GB, IE, NL, DE, IL
Traffic rank or commercial relevance filters where available
```

**Search set C: company docs / technical surface**

```text
Technology or keyword combinations:
Datadog + "AI"
Cloudflare + "copilot"
Segment + "assistant"
Snowflake + "RAG"
```

**Expected lead volume**

- `25-45` accounts worth importing to Clay
- Usually `10-25` contacts after contact sourcing

**Quality vs. quantity**

- Good for discovery
- Moderate signal quality for AI specifically
- Treat as `readiness proxy`, not definitive AI-stack evidence

### GitHub Search

**Why use it**

- Best source for `public technical proof`
- Good for identifying companies with engineering teams publishing around `LLMs`, `platform`, `observability`, `inference`, or `MLOps`
- Lower volume but highest technical precision

**GitHub search pattern**

Use GitHub in two ways:

1. `Discovery`: find companies with public AI / infra repositories or topics
2. `Validation`: confirm that a sourced account has public technical evidence

**Code search query: AI infra evidence**

Run in GitHub code search.

```text
("aws bedrock" OR "vertex ai" OR "azure openai" OR langchain OR llamaindex OR vllm OR mlflow OR opentelemetry OR triton OR ray)
(language:python OR language:typescript OR language:go)
NOT path:/vendor/
NOT path:/node_modules/
NOT is:fork
```

**Code search query: observability and latency evidence**

```text
("p95" OR "p99" OR "latency" OR "inference" OR "observability" OR "evaluation")
(language:python OR language:typescript OR language:go)
NOT path:/vendor/
NOT is:fork
```

**Org validation query**

After you know or infer a GitHub org:

```text
org:{{github_org}}
(langchain OR llamaindex OR vllm OR mlflow OR opentelemetry OR "aws bedrock" OR "vertex ai" OR "azure openai")
NOT path:/vendor/
NOT is:fork
```

**Repository topic discovery**

Use GitHub topic pages and repository metadata to discover organizations in:

```text
topic:llm
topic:rag
topic:mlops
topic:observability
topic:kubernetes
topic:developer-tools
```

**Expected lead volume**

- `15-30` high-fit accounts
- `10-20` usable contacts after enrichment

**Quality vs. quantity**

- Highest quality for technical-fit validation
- Lowest scale
- Best used as an account-priority signal, not a primary people database

### Crunchbase

**Why use it**

- Best for `funding stage`, `funding recency`, `growth`, and `market narrative`
- Useful for building urgency queues before contact sourcing
- Especially strong for Series A-C and growth-stage private companies

**Crunchbase search filters**

Build separate saved lists by vertical.

```text
Entity type:
Organizations / Companies

Headquarters:
United States
Canada
United Kingdom
Ireland
Germany
Netherlands
Israel

Categories:
Artificial Intelligence
Developer Tools
FinTech
Cyber Security
Health Care
Customer Service

Funding round type:
Series A
Series B
Series C
Series D
Growth / Late Stage Venture

Last funding announced:
Last 18 months

Employee estimate:
201-5000
```

**Trigger-oriented saved searches**

```text
Search 1:
Series B/C in last 9 months + AI / Developer Tools

Search 2:
Series A-D in last 12 months + FinTech / Security / Healthtech

Search 3:
Recently mentioned in news + AI expansion language + employee growth
```

**Expected lead volume**

- `25-45` account-quality additions to the master list

**Quality vs. quantity**

- Strong company-level fit and urgency
- Weak contact-level data
- Best paired with Apollo or Sales Nav for people sourcing

## 2. CLAY TABLE SCHEMA

Build this as a two-table workflow:

- `Accounts_Master`
- `Contacts_Master`

If your team prefers a single export table, keep both tables but write a final flattened view to `Contacts_Export`.

### Accounts_Master

| Column Name | Data Type | Source | Why It Matters For ICP Scoring |
|---|---|---|---|
| `company_name` | string | Apollo / Sales Nav / Crunchbase / BuiltWith | Primary account identifier |
| `domain` | string | Apollo / BuiltWith / Clay formula normalization | Primary dedupe key and scoring join key |
| `root_domain` | string | Clay formula | Normalizes duplicates across subdomains |
| `company_website_url` | url | Apollo / BuiltWith | QA and manual validation |
| `company_linkedin_url` | url | Apollo / Sales Nav | Validation and teammate review |
| `sales_nav_account_url` | url | Sales Nav | Preserves exact source account |
| `apollo_account_id` | string | Apollo | Stable source identifier |
| `crunchbase_company_url` | url | Crunchbase | Funding verification |
| `industry` | string | Apollo / Crunchbase / LinkedIn | Maps to `industry_fit` |
| `market_segment` | string | Apollo | Useful for segment routing and disqualification |
| `hq_country` | string | Apollo / Sales Nav / Crunchbase | Geo segmentation |
| `hq_city` | string | Apollo / Sales Nav | Geo segmentation |
| `headcount` | number | Apollo / LinkedIn / Crunchbase | Maps to `headcount_fit` |
| `headcount_band` | string | Clay formula | Simplifies scoring logic |
| `employee_growth_signal` | string | Apollo / Crunchbase | Optional growth / urgency input |
| `founded_year` | number | Apollo / Crunchbase | Contextual validation |
| `funding_stage` | string | Crunchbase first, Apollo fallback | Maps to `funding_stage` |
| `last_funding_date` | date | Crunchbase first, Apollo fallback | Used for urgency |
| `funding_recency_months` | number | Clay formula | Maps to `business_urgency` |
| `total_funding_usd` | currency | Crunchbase | Budget proxy |
| `arr_estimate` | string / number | Crunchbase / manual / web research | Optional input for monetization pressure |
| `builtwith_tech_raw` | json / string | BuiltWith | Raw stack evidence |
| `apollo_technologies_raw` | json / string | Apollo | Raw stack evidence |
| `tech_stack_normalized` | string | Clay formula combining BuiltWith + Apollo + GitHub | Maps to `ai_in_production` and `inference_complexity` |
| `ai_stack_signal_count` | number | Clay formula | Faster prioritization |
| `github_org` | string | GitHub search / Clay formula / manual QA | Enables GitHub validation |
| `github_org_url` | url | GitHub | Manual review and reproducibility |
| `github_repo_count` | number | GitHub API | Technical maturity proxy |
| `github_last_push_date` | date | GitHub API | Activity recency |
| `github_ai_repo_hits` | number | GitHub search / HTTP API | AI-in-production validation |
| `github_activity_score` | number | Clay formula | Technical intensity proxy |
| `ai_job_postings_90d` | number | Apollo first, LinkedIn Jobs fallback | Maps to `ai_job_postings` |
| `ai_job_titles_90d` | string / list | Apollo / LinkedIn / public jobs pages | Helps validate workload type |
| `job_postings_source` | string | Clay manual / formula | Provenance |
| `recent_trigger` | string | Clay formula using funding/jobs/GitHub/news | Maps to `business_urgency` and monetization proxy |
| `lead_source_platforms` | string / list | Clay formula | Traceability |
| `source_query_name` | string | Manual | Tells a teammate exactly which search produced the row |
| `account_validation_status` | string | Clay formula / manual | `pass`, `review`, `reject` |

### Contacts_Master

| Column Name | Data Type | Source | Why It Matters For ICP Scoring |
|---|---|---|---|
| `company_name` | string | Lookup from Accounts_Master | Flattened export field |
| `domain` | string | Lookup from Accounts_Master | Export + join key |
| `contact_name` | string | Apollo / Sales Nav | Required outreach field |
| `first_name` | string | Apollo / Clay formula | Outreach personalization |
| `last_name` | string | Apollo / Clay formula | Outreach personalization |
| `contact_title` | string | Apollo first, Sales Nav validator | Maps to `title_match` |
| `seniority` | string | Apollo / Sales Nav | Buyer qualification |
| `department` | string | Apollo / Sales Nav | Helps exclude non-buyers |
| `contact_linkedin_url` | url | Apollo / Sales Nav | Manual QA and LinkedIn outreach |
| `contact_email` | string | Clay waterfall | Email outreach |
| `email_status` | string | Clay waterfall provider / verifier | Deliverability gating |
| `email_source` | string | Clay waterfall | Provenance |
| `phone_number` | string | Optional Clay waterfall | Optional multi-channel |
| `apollo_contact_id` | string | Apollo | Stable source identifier |
| `sales_nav_lead_url` | url | Sales Nav | Validation and teammate handoff |
| `buyer_fit_status` | string | Clay formula | `primary`, `secondary`, `reject` |
| `lead_source_platform` | string | Clay formula | Attribution |
| `source_query_name` | string | Manual / copied from source table | Reproducibility |
| `contact_validation_status` | string | Clay formula / manual | QA gating before export |

### Contacts_Export

This should be the final flat export table used by the Python scoring pipeline.

**Minimum required export columns**

```text
company_name
domain
headcount
funding_stage
funding_recency_months
tech_stack
ai_job_postings_90d
contact_name
contact_title
contact_email
contact_linkedin
industry
recent_trigger
```

## 3. CLAY ENRICHMENT WATERFALL

### Workbook Layout

Use one Clay workbook with these tabs:

```text
01_Apollo_Accounts_Seed
02_SalesNav_Accounts_Seed
03_BuiltWith_Accounts_Seed
04_Crunchbase_Accounts_Seed
05_GitHub_Accounts_Seed
06_Accounts_Master
07_Contacts_Master
08_Contacts_Export
```

### Step-by-Step Enrichment Sequence

#### Step 1: Source account seeds

Import each platform’s output into its own seed table.

Required source columns:

```text
company_name
domain_or_website
source_platform
source_query_name
source_url
```

#### Step 2: Normalize company identity

In each seed table, create `root_domain`, then merge all seed tabs into `06_Accounts_Master` and dedupe by `root_domain`.

**Clay formula: root domain**

```javascript
(() => {
  const raw = {{domain_or_website}} || {{domain}} || {{company_website_url}} || "";
  const cleaned = raw
    .toString()
    .toLowerCase()
    .replace(/^https?:\/\//, "")
    .replace(/^www\./, "")
    .split("/")[0]
    .trim();
  return cleaned;
})()
```

#### Step 3: Enrich firmographics

Run this order on `Accounts_Master`:

1. `Apollo` account enrichment by domain
2. `Crunchbase` enrichment by company or domain
3. `LinkedIn / Sales Nav` manual validator for account URL if still null

**Waterfall rule**

```text
headcount = Apollo.headcount -> LinkedIn.company_size -> Crunchbase.employee_estimate
industry = Apollo.industry -> Crunchbase.category -> LinkedIn.industry
funding_stage = Crunchbase.last_round_stage -> Apollo.stage
last_funding_date = Crunchbase.last_funding_date -> Apollo.last_funding_date
```

#### Step 4: Enrich tech stack

Run this order:

1. `BuiltWith` by domain
2. `Apollo Technologies`
3. `GitHub technical validation`

**Clay formula: normalized tech stack**

```javascript
(() => {
  const raw = [
    {{builtwith_tech_raw}} || "",
    {{apollo_technologies_raw}} || "",
    {{github_ai_stack_terms}} || ""
  ].join(", ").toLowerCase();

  const signals = [
    "openai", "anthropic", "aws bedrock", "vertex ai", "azure openai",
    "langchain", "llamaindex", "mlflow", "ray", "vllm", "triton",
    "datadog", "langsmith", "opentelemetry", "kubernetes"
  ];

  return signals.filter(signal => raw.includes(signal)).join(", ");
})()
```

#### Step 5: Enrich GitHub org activity

First infer `github_org` from company data. Then use GitHub HTTP enrichments.

**Inference order**

1. Direct GitHub org URL from source row
2. Company domain slug guess
3. LinkedIn company vanity guess
4. Manual QA only for top-priority rows

**HTTP API snippet: list org repositories**

```http
GET https://api.github.com/orgs/{{github_org}}/repos?type=public&sort=updated&per_page=100
Accept: application/vnd.github+json
Authorization: Bearer {{GITHUB_TOKEN}}
X-GitHub-Api-Version: 2026-03-10
```

Suggested field paths:

```text
repo_count = length(response)
github_last_push_date = max(response[].pushed_at)
github_repo_names = response[].name
```

**HTTP API snippet: search code for AI / infra terms**

```http
GET https://api.github.com/search/code?q=org:{{github_org}}+(langchain+OR+llamaindex+OR+vllm+OR+mlflow+OR+opentelemetry+OR+"aws+bedrock"+OR+"vertex+ai"+OR+"azure+openai")+NOT+path:vendor&per_page=100
Accept: application/vnd.github+json
Authorization: Bearer {{GITHUB_TOKEN}}
X-GitHub-Api-Version: 2026-03-10
```

Suggested field paths:

```text
github_ai_repo_hits = response.total_count
github_ai_stack_terms = response.items[].repository.name
```

**Clay formula: GitHub activity score**

```javascript
(() => {
  const repoCount = Number({{github_repo_count}} || 0);
  const aiHits = Number({{github_ai_repo_hits}} || 0);
  const lastPush = {{github_last_push_date}};

  let score = 0;
  if (repoCount >= 20) score += 2;
  if (repoCount >= 50) score += 1;
  if (aiHits >= 3) score += 4;
  if (aiHits >= 10) score += 2;

  if (lastPush) {
    const days = moment().diff(moment(lastPush), "days");
    if (days <= 30) score += 2;
    else if (days <= 90) score += 1;
  }

  return score;
})()
```

#### Step 6: Enrich AI job postings

Run this order:

1. `Apollo Job Postings`
2. `LinkedIn Jobs` manual / assisted
3. Public careers page / Greenhouse / Lever HTTP pulls for top accounts only

**Apollo titles to use**

```text
Machine Learning Engineer
ML Platform Engineer
AI Platform Engineer
Inference Engineer
MLOps Engineer
Staff Machine Learning Engineer
Platform Engineer
Applied AI Engineer
```

**Clay formula: AI jobs count within 90 days**

If raw jobs are stored as a list or JSON string:

```javascript
(() => {
  const raw = ({{ai_job_titles_90d}} || "").toString().toLowerCase();
  if (!raw) return 0;

  const patterns = [
    "machine learning engineer",
    "ml platform engineer",
    "ai platform engineer",
    "inference engineer",
    "mlops engineer",
    "applied ai engineer",
    "platform engineer"
  ];

  let count = 0;
  patterns.forEach(pattern => {
    if (raw.includes(pattern)) count += 1;
  });
  return count;
})()
```

#### Step 7: Generate recent trigger string

**Clay formula: recent trigger**

```javascript
(() => {
  const triggers = [];
  const months = Number({{funding_recency_months}} || 999);
  const stage = {{funding_stage}} || "";
  const jobs = Number({{ai_job_postings_90d}} || 0);
  const aiHits = Number({{github_ai_repo_hits}} || 0);

  if (months <= 9 && stage) triggers.push(`Raised ${stage} ${months}mo ago`);
  if (jobs >= 3) triggers.push(`${jobs} AI/platform roles open in last 90d`);
  if (aiHits >= 3) triggers.push(`Public GitHub activity shows ${aiHits} AI/infra code hits`);
  if (({{tech_stack_normalized}} || "").toString().includes("vllm")) triggers.push("Uses vLLM or similar inference-serving tooling");
  if (({{tech_stack_normalized}} || "").toString().includes("opentelemetry")) triggers.push("Has AI observability / telemetry signal");

  return triggers.join(" | ");
})()
```

#### Step 8: Source contacts

Run contacts only on rows in `Accounts_Master` where:

```text
headcount >= 200
AND account_validation_status != reject
AND (tech_stack_normalized is not empty OR ai_job_postings_90d >= 1 OR funding_recency_months <= 18)
```

**Contact waterfall**

1. `Apollo People` from saved account list
2. `Sales Nav` lead validation and gap fill
3. `Clay work email waterfall`

**Title targeting**

```text
CTO
Chief Technology Officer
VP Engineering
Vice President Engineering
SVP Engineering
Head of Engineering
Head of Platform
Head of Infrastructure
```

#### Step 9: Email waterfall

Use Clay’s work-email waterfall for top validated contacts only.

**Run condition**

```javascript
!!{{contact_name}} &&
!!{{domain}} &&
["CTO","VP Engineering","Vice President Engineering","SVP Engineering","Head of Engineering","Head of Platform","Head of Infrastructure"]
  .some(title => ({{contact_title}} || "").includes(title))
```

**Recommended order**

1. Apollo email
2. Dropcontact / Hunter / Prospeo / Datagma via Clay waterfall
3. Only keep `valid` or `accept_all` if the lead is otherwise high-fit

#### Step 10: Write final export table

Push only validated rows to `Contacts_Export`.

## 4. DATA QUALITY RULES

### Validation checks before a row enters scoring

| Check | Rule | Action if Failed |
|---|---|---|
| Domain present | `domain` or `root_domain` must be non-empty | Reject row |
| Company name present | `company_name` must be non-empty | Reject row |
| Headcount valid | Numeric and `>= 100` for export; prefer `>= 200` | Mark `review` if 100-199, reject if missing and no fallback |
| Industry valid | Must map to a known category or be manually normalized | Set `other` if missing, do not block |
| Contact title valid | Must match primary or secondary engineering persona | Reject non-technical titles |
| LinkedIn or email present | Need at least one outreach path | Reject if both missing |
| Funding fields normalized | `funding_stage` and `funding_recency_months` should be parseable | Set `unknown` / `999` if missing |
| Tech stack normalized | `tech_stack_normalized` should be a comma-separated string | Allow null, but mark `review` if no other AI signals |
| Job posting count numeric | `ai_job_postings_90d` must be integer | Default to `0` |
| Duplicate contacts removed | Dedupe on `root_domain + normalized_title + linkedin_url_or_email` | Keep best-validated row |

### Missing-field handling

| Missing Field | Handling Rule |
|---|---|
| `headcount` | Fallback Apollo -> LinkedIn -> Crunchbase; if still missing, mark `review` |
| `funding_stage` | Set to `unknown`; do not block export if strong AI + title signals exist |
| `funding_recency_months` | Set to `999`; scoring logic should award `0` urgency from funding |
| `tech_stack_normalized` | Fallback BuiltWith -> Apollo -> GitHub; if still empty, allow export only if job postings or trigger is strong |
| `github_org` | Leave blank; do not block export |
| `ai_job_postings_90d` | Set `0`; do not block |
| `contact_email` | Keep row if `contact_linkedin_url` exists so it can be used for LinkedIn outreach |
| `contact_linkedin_url` | Keep row if email is valid, but mark `review` for top-tier outreach |

### Dedupe policy

**Accounts**

```text
Primary key = root_domain
Fallback = company_name + hq_country
```

**Contacts**

```text
Primary key = linkedin_url
Fallback = lower(email)
Fallback 2 = lower(company_name) + lower(contact_name) + normalized_title
```

**Survivorship**

Keep the row with the highest quality in this order:

```text
1. Sales Nav validated title
2. Valid email
3. Non-null LinkedIn URL
4. Non-null tech stack
5. Non-null funding data
```

## 5. REPRODUCIBILITY CHECKLIST

Run this checklist monthly with the same naming conventions.

### Saved Search Naming Convention

```text
P95 | Apollo Accounts | AI-DevTools | YYYY-MM
P95 | Apollo Accounts | Fintech-Security-Health | YYYY-MM
P95 | Apollo People | Primary Buyers | YYYY-MM
P95 | SalesNav Accounts | AI-DevTools | YYYY-MM
P95 | SalesNav Accounts | Fintech-Security-Health | YYYY-MM
P95 | SalesNav Leads | Primary Buyers | YYYY-MM
P95 | BuiltWith | Tech-Maturity | YYYY-MM
P95 | Crunchbase | Funded Growth Accounts | YYYY-MM
P95 | GitHub | AI Infra Orgs | YYYY-MM
```

### Monthly Runbook

1. Duplicate the previous Clay workbook and rename it:

```text
P95 Lead Sourcing | YYYY-MM
```

2. Clear only source rows and output rows.
   Keep formulas, enrichment columns, and validation logic intact.

3. Export fresh source lists:

```text
Apollo companies
Apollo people
Sales Nav accounts
Sales Nav leads
BuiltWith account list
Crunchbase account list
GitHub account list
```

4. Import each source list into its matching seed tab.

5. Verify each source tab contains:

```text
company_name
domain_or_website
source_platform
source_query_name
source_url
```

6. Run `root_domain` normalization in every seed table.

7. Append all seed tables into `06_Accounts_Master`.

8. Dedupe `Accounts_Master` on `root_domain`.

9. Run firmographic enrichments in this order:

```text
Apollo -> Crunchbase -> LinkedIn/Sales Nav manual account validator
```

10. Run stack enrichments in this order:

```text
BuiltWith -> Apollo Technologies -> GitHub validation
```

11. Run job-posting enrichment:

```text
Apollo Job Postings -> LinkedIn Jobs manual / public careers fallback
```

12. Recalculate:

```text
funding_recency_months
tech_stack_normalized
ai_stack_signal_count
github_activity_score
recent_trigger
account_validation_status
```

13. Filter `Accounts_Master` down to rows where:

```text
account_validation_status = pass OR review
```

14. Source contacts only for those filtered accounts.

15. Run title validation and set:

```text
buyer_fit_status = primary / secondary / reject
```

16. Run the email waterfall only on `primary` or `secondary` buyers.

17. Dedupe `Contacts_Master`.

18. Push valid rows to `08_Contacts_Export`.

19. Confirm the final export contains the Python pipeline schema:

```text
company_name
domain
headcount
funding_stage
funding_recency_months
tech_stack
ai_job_postings_90d
contact_name
contact_title
contact_email
contact_linkedin
industry
recent_trigger
```

20. Export the final CSV to:

```text
data/raw_leads.csv
```

21. Run the scoring pipeline locally:

```bash
python3 score_leads.py \
  --input data/raw_leads.csv \
  --output output/scored_leads.csv \
  --report \
  --top 50
```

22. Archive the following alongside the CSV:

```text
saved search screenshots or URLs
Clay workbook URL
date run
owner
notes on any manual overrides
```

## Appendix: Notes On Platform Reliability

- `Apollo` is the best primary source because it combines account, people, technologies, and job-posting filters in one workflow.
- `Sales Navigator` should be treated as the highest-trust title validator.
- `BuiltWith` should be treated as a discovery and readiness-proxy source, not final proof of backend AI infrastructure.
- `GitHub` should be treated as public technical proof and prioritization signal.
- `Crunchbase` should be treated as the primary funding and recency authority.

