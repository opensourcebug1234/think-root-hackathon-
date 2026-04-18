"""
mock_leads.py — Generate realistic mock leads for testing the pipeline

Usage:
    python mock_leads.py                        # generates 220 leads to data/raw_leads.csv
    python mock_leads.py --count 50 --output data/test.csv
"""

import argparse
import random
import pandas as pd
import os

random.seed(42)

# ---- Sample data pools ----

COMPANIES = [
    ("Cerebral AI", "cerebral.ai", "AI/ML"), ("Vantage Labs", "vantage.io", "SaaS"),
    ("Meridian Health", "meridianhealth.com", "Healthtech"), ("Qubit Finance", "qubitfin.com", "Fintech"),
    ("Axle Data", "axledata.io", "DevTools"), ("Neon Systems", "neonsystems.ai", "AI/ML"),
    ("Cascade ML", "cascademl.com", "AI/ML"), ("Omni Commerce", "omnicommerce.io", "Ecommerce"),
    ("Prism Analytics", "prismanalytics.com", "SaaS"), ("Forge Security", "forgesec.io", "SaaS"),
    ("Orion Robotics", "orionrobotics.ai", "AI/ML"), ("Delphi Labs", "delphilabs.io", "DevTools"),
    ("Nova Fintech", "novafintech.com", "Fintech"), ("Apex Health AI", "apexhealthai.com", "Healthtech"),
    ("Helix Data", "helixdata.io", "AI/ML"), ("Summit SaaS", "summitsaas.com", "SaaS"),
    ("Ember AI", "emberai.co", "AI/ML"), ("Pulse Analytics", "pulseanalytics.io", "SaaS"),
    ("Stratum Cloud", "stratumcloud.com", "DevTools"), ("Vector Labs", "vectorlabs.ai", "AI/ML"),
    ("Cobalt Finance", "cobaltfin.io", "Fintech"), ("Horizon Health", "horizonhealth.ai", "Healthtech"),
    ("Drift Commerce", "driftcommerce.com", "Ecommerce"), ("Zenith ML", "zenithml.io", "AI/ML"),
    ("Keystone Tech", "keystonetech.com", "SaaS"), ("Radiant AI", "radiantai.co", "AI/ML"),
    ("Atlas DevTools", "atlasdev.io", "DevTools"), ("Pinnacle Finance", "pinnaclefin.com", "Fintech"),
    ("CoreHealth", "corehealth.ai", "Healthtech"), ("Luminary SaaS", "luminarysaas.com", "SaaS"),
]

TECH_STACKS = [
    "openai,pytorch,kubernetes,aws",
    "anthropic,langchain,aws bedrock,kubernetes",
    "openai,llamaindex,hugging face,gcp",
    "pytorch,tensorflow,sagemaker,aws",
    "openai,mlflow,ray,azure",
    "vertex ai,tensorflow,gcp,kubernetes",
    "vllm,pytorch,aws,kubernetes",
    "openai,fastapi,redis,aws",
    "hugging face,pytorch,mlflow,azure",
    "cohere,langchain,aws,docker",
    "tensorflow,sagemaker,aws,kubernetes",
    "openai,together ai,ray,aws",
    "pytorch,triton,kubernetes,gcp",
    "anthropic,llamaindex,aws bedrock,fastapi",
    "django,postgres,aws",               # weak signal
    "node.js,mongodb,heroku",            # no AI signal
    "react,firebase,gcp",               # no AI signal
]

FUNDING_STAGES = [
    "Series B", "Series C", "Series A", "Series D",
    "Growth", "Seed", "Series B", "Series C", "Series B",  # weighted toward B/C
]

TITLES = [
    "CTO", "VP Engineering", "VP of Engineering", "Head of Engineering",
    "Director of Engineering", "Principal Engineer", "Engineering Manager",
    "Senior Software Engineer", "CTO", "VP Engineering",  # weighted toward CTO/VP
]

FIRST_NAMES = ["Arjun", "Priya", "Rahul", "Ananya", "Vikram", "Deepa", "Siddharth", "Nisha",
               "James", "Sarah", "Michael", "Emily", "David", "Jessica", "Robert", "Amanda",
               "Wei", "Mei", "Zhang", "Lin", "Yuki", "Kenji", "Aiko", "Hiroshi"]

LAST_NAMES  = ["Sharma", "Patel", "Iyer", "Gupta", "Reddy", "Nair", "Kumar", "Singh",
               "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
               "Chen", "Wang", "Liu", "Zhang", "Yamamoto", "Tanaka", "Sato", "Watanabe"]

TRIGGERS = [
    "Raised Series B 3 months ago",
    "Posted 8 ML Engineer roles in last 30 days",
    "Launched new AI product feature last quarter",
    "CTO joined from OpenAI 6 months ago",
    "Raised Series C 2 months ago — aggressive hiring",
    "Engineering blog post on LLM latency issues published last week",
    "Expanded from 200 to 350 employees in 6 months",
    None, None, None,  # some leads have no trigger
]


def generate_leads(count: int) -> pd.DataFrame:
    rows = []
    companies_pool = COMPANIES * (count // len(COMPANIES) + 1)
    random.shuffle(companies_pool)

    for i in range(count):
        company_name, domain, industry = companies_pool[i % len(companies_pool)]
        # Add index to make company names unique
        if i >= len(COMPANIES):
            company_name = f"{company_name} {i}"

        headcount = random.choice([
            random.randint(20, 100),
            random.randint(100, 500),
            random.randint(500, 2000),
            random.randint(2000, 5000),
        ])

        funding_stage     = random.choice(FUNDING_STAGES)
        funding_recency   = random.randint(1, 36)
        tech_stack        = random.choice(TECH_STACKS)
        ai_job_postings   = random.choice([0, 0, 1, 2, 3, 5, 7, 10, 12, 15])
        contact_name      = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        contact_title     = random.choice(TITLES)
        contact_email     = f"{contact_name.split()[0].lower()}.{contact_name.split()[1].lower()}@{domain}"
        contact_linkedin  = f"https://linkedin.com/in/{contact_name.replace(' ', '-').lower()}"
        recent_trigger    = random.choice(TRIGGERS)

        rows.append({
            "company_name":            company_name,
            "domain":                  domain,
            "headcount":               headcount,
            "funding_stage":           funding_stage,
            "funding_recency_months":  funding_recency,
            "tech_stack":              tech_stack,
            "ai_job_postings_90d":     ai_job_postings,
            "contact_name":            contact_name,
            "contact_title":           contact_title,
            "contact_email":           contact_email,
            "contact_linkedin":        contact_linkedin,
            "industry":                industry,
            "recent_trigger":          recent_trigger if recent_trigger else "",
        })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate mock leads CSV for testing")
    parser.add_argument("--count",  type=int, default=220, help="Number of leads to generate")
    parser.add_argument("--output", default="data/raw_leads.csv", help="Output CSV path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    df = generate_leads(args.count)
    df.to_csv(args.output, index=False)
    print(f"Generated {len(df)} mock leads → {args.output}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()
