# P95.AI Ideal Customer Profile (ICP)

## 1. FIRMOGRAPHICS

### Company Size

| Segment | Headcount | ARR Range | Fit | Why It Matters |
|---|---:|---:|---|---|
| Core ICP | 200-3,000 employees | $20M-$500M ARR | High | Big enough to have production AI traffic, budget, and a real platform problem; still agile enough to buy point solutions fast. |
| Best-Fit Band | 400-2,000 employees | $50M-$250M ARR | Highest | Usually has dedicated platform, ML, or infra leaders and clear pressure to improve latency, reliability, and gross margin. |
| Strategic Enterprise | 3,000-10,000 employees | $500M+ ARR | Medium | Strong budget and scale, but slower procurement and greater preference for platform standardization. |
| Below Floor | Under 150 employees | Under $15M ARR | Low | Usually still experimenting, not yet feeling inference cost and SLO pain at enterprise scale. |

### Industry Verticals (Top 5, Ranked by Fit)

| Rank | Vertical | Why It Fits P95.AI |
|---|---|---|
| 1 | AI-native SaaS and developer tooling | Inference performance is product performance; latency, uptime, and unit economics directly affect retention and gross margin. |
| 2 | Customer support, conversational AI, and contact-center software | High-volume real-time workloads make p95/p99 latency, routing quality, and cost per interaction highly visible. |
| 3 | Fintech, payments, and insurtech | Strong uptime and compliance expectations, frequent fraud/risk use cases, and material sensitivity to reliability regressions. |
| 4 | Cybersecurity platforms | AI copilots, alert triage, and investigation workflows create heavy inference demand and require trustworthy, low-latency responses. |
| 5 | Healthtech and clinical/admin automation | Mission-critical workflows, strict reliability expectations, and growing AI workloads in support, documentation, and operations. |

### Tech Stack Signals That Indicate Readiness

| Signal Strength | Signal | Why It Matters |
|---|---|---|
| Very strong | Uses AWS Bedrock, Vertex AI, or Azure OpenAI / Azure AI Foundry | Indicates a company has moved beyond experimentation and is deploying or managing foundation-model inference on a major cloud platform. |
| Very strong | Self-hosts or serves models with vLLM, Triton, Ray Serve, KServe, or Kubernetes GPU infrastructure | Strong sign that latency, throughput, and cost optimization are now platform problems, not just app problems. |
| Very strong | Publicly references LLMs, copilots, agents, RAG, or generative AI features as GA or production | Confirms revenue-adjacent AI usage and real end-user expectations. |
| Strong | Uses LangSmith, Datadog LLM Observability, OpenTelemetry GenAI tracing, MLflow, Weights & Biases, or custom eval pipelines | Suggests a team is operationalizing AI and cares about monitoring, regressions, and production debugging. |
| Strong | Hiring for ML platform, inference engineer, AI platform engineer, or staff-level platform roles | Signals active investment in production AI systems and likely organizational urgency. |
| Medium | Public engineering content about model routing, prompt optimization, GPU utilization, caching, or fallback policies | Indicates the team is already working on the exact problems P95.AI helps solve. |

### Funding Stage and Recency Signals

| Signal | Fit | Why It Matters |
|---|---|---|
| Series A to Series C | High | Enough capital to fund AI teams and vendor spend, with strong pressure to scale product usage efficiently. |
| Series D+, growth equity, or PE-backed scale-up | Medium-High | Budget exists, but buying process is longer and value proof must be tied to efficiency or SLA protection. |
| Public company with a visible AI revenue line or cost-efficiency mandate | Medium | Strong pain and budget, but usually needs a more mature multi-stakeholder sales motion. |
| Funding in last 0-9 months | Highest | Fresh budget plus pressure to convert AI narrative into operational results quickly. |
| Funding in last 10-18 months | High | Still actionable, especially if paired with hiring growth or new AI launches. |
| No recent funding, but new AI product launch or major AI hiring burst | High | For established companies, product expansion often matters more than fundraising. |

## 2. BUYER PERSONA — PRIMARY (CTO / VP Eng)

### Day-to-Day Pain Points Around AI in Production

- Tail latency spikes at p95/p99 that make AI features feel unreliable even when average latency looks fine.
- Rising inference spend from overprovisioned GPUs, poor model routing, redundant context, or fallback chains.
- Limited visibility into why output quality, latency, or cost changes after prompt, model, or traffic shifts.
- Pressure to ship new AI features quickly without introducing outages, regressions, or runaway cloud bills.
- Difficulty balancing quality, speed, and cost across multiple model vendors and deployment paths.
- Incident fatigue caused by opaque failures in retrieval, orchestration, rate limits, or model-provider dependencies.

### KPIs They Own

- p95 and p99 latency for AI endpoints
- Availability and uptime for AI-powered product surfaces
- Error rate, timeout rate, and incident frequency
- Cost per inference, cost per active user, or GPU / token spend efficiency
- Gross margin impact of AI features
- MTTR for AI incidents and regressions
- Release velocity for AI features without reliability degradation

### Trigger Events That Create Urgency

- New funding round or board pressure to prove AI monetization
- Launch of an AI copilot, assistant, agent, or RAG feature into general availability
- Rapid hiring of ML platform, infra, or AI product engineering roles
- A public or internal AI incident: outage, hallucination spike, response slowdown, or cloud-cost surprise
- Migration between model providers or move from API-only usage to hybrid/self-hosted inference
- Enterprise deal pressure where latency, uptime, or security reviews become blockers
- FinOps or CFO mandate to improve margin on AI-heavy product lines

### Channels They Trust

They trust operator-heavy channels more than generic vendor marketing. The most credible places to reach them are technical communities, practitioner conferences, engineering postmortems, and implementation-focused newsletters.

**Conferences**

- AI Engineer World’s Fair
- KubeCon + CloudNative AI Day
- AWS re:Invent
- Google Cloud Next

**Newsletters and Media**

- Latent Space
- The Sequence
- InfoQ AI, ML & Data Engineering

**Communities**

- MLOps Community
- CNCF and Kubernetes practitioner circles
- GitHub issues, discussions, and maintainer ecosystems around tools like vLLM, Ray, LangChain, and OpenTelemetry

## 3. NEGATIVE ICP (disqualifiers)

| Disqualifier | Why They Are Not Worth Targeting |
|---|---|
| Pre-seed startups or teams under 50 employees | Usually pre-optimization. They have experimentation pain, not sustained production-inference pain. |
| Companies using AI only for internal productivity or basic chatbots | Low urgency, small workloads, weak ROI case, and limited buyer motivation around latency or cost at scale. |
| Services firms, agencies, and consultancies without a repeatable software product | Inference spend is not concentrated in a single scaled product surface; pain is fragmented and harder to monetize. |
| Non-technical verticals with no clear AI product or engineering-led motion | No credible owner for latency, reliability, or inference optimization. |
| Companies with zero public AI stack signals and zero AI hiring | High likelihood of being in exploration mode only. |
| Very large incumbents with fully internal model-optimization teams and hard platform lock-in | Can still be strategic, but often require a long enterprise transformation sale rather than a focused pain sale. |
| Buyer titles outside engineering, platform, ML, or infrastructure leadership | The economic pain sits with technical leadership, so non-technical contacts create slow or misaligned cycles. |

## 4. LEAD SCORING RUBRIC

Score each lead from 0-100. Assign the full weight when the lead strongly matches the criterion, half weight when evidence is partial, and zero when absent or contradictory.

**Tier classification**

- `Hot`: 75+
- `Warm`: 50-74
- `Cold`: <50

| Criterion | Weight | What Good Looks Like | How To Verify From Public Data |
|---|---:|---|---|
| AI-in-production stack evidence | 20 | Cloud AI platforms, model-serving infra, or public proof of LLMs in production | Engineering blog, docs, case studies, BuiltWith/Wappalyzer, GitHub repos, cloud partner pages |
| Inference scale and complexity | 15 | Multi-model usage, self-hosting, Kubernetes/GPU infra, routing, caching, evals, or real-time AI UX | Job posts, engineering blog, architecture talks, GitHub repos, conference speaker bios |
| AI observability and reliability maturity | 10 | Use of LangSmith, Datadog LLM Observability, OpenTelemetry GenAI, MLflow, or internal monitoring patterns | Docs, repos, engineering posts, telemetry libraries, public dashboards, conference talks |
| AI hiring velocity | 10 | 3+ AI/ML/platform roles in the last 90 days or a sustained hiring pattern | Greenhouse / Lever / company careers page / LinkedIn Jobs |
| Company headcount fit | 10 | 200-3,000 employees, with best scores in the 400-2,000 range | LinkedIn company profile, company website, Apollo, Clay, ZoomInfo, Crunchbase profile |
| ARR and monetization pressure | 10 | Meaningful software revenue plus AI features tied to product adoption or margin | Public filings, investor materials, pricing pages, analyst coverage, interviews, press releases |
| Funding stage fit | 8 | Series A-C or growth-stage company with budget and scale pressure | Crunchbase, company press releases, investor announcements |
| Funding recency or business urgency | 7 | Raise in past 18 months, major AI launch, or AI cost/reliability pressure called out publicly | Crunchbase, press releases, newsroom, product launch posts, executive interviews |
| Industry fit | 5 | Operates in one of the top five high-fit verticals | Company website, Crunchbase category, LinkedIn description |
| Buyer title match | 5 | CTO, VP Engineering, SVP Engineering, Head of Platform, or equivalent | LinkedIn, company leadership page, conference speaker pages |

### Practical Scoring Notes

| Criterion | Max Score Guidance |
|---|---|
| AI-in-production stack evidence | 20 = multiple strong signals; 10 = one strong signal or several medium signals; 0 = no evidence |
| Inference scale and complexity | 15 = self-hosted or multi-provider complexity is visible; 8 = moderate production complexity; 0 = unclear |
| AI observability and reliability maturity | 10 = explicit observability/evals stack; 5 = indirect reliability tooling; 0 = absent |
| AI hiring velocity | 10 = 5+ relevant roles or dedicated AI platform hiring; 5 = 1-4 roles; 0 = none |
| Company headcount fit | 10 = 400-2,000; 7 = 200-399 or 2,001-3,000; 3 = 100-199; 0 = below 100 unless other signals are exceptional |
| ARR and monetization pressure | 10 = AI is revenue-critical or margin-critical; 5 = company has scale but AI economics are not yet visible; 0 = unclear |
| Funding stage fit | 8 = Series A-C or strong growth-stage; 4 = public or late-stage but slower-moving; 0 = pre-seed/bootstrapped with low scale |
| Funding recency or business urgency | 7 = raise or major AI trigger in last 9 months; 4 = 10-18 months; 2 = older but still active AI expansion; 0 = none |
| Industry fit | 5 = top 2 verticals; 3 = ranks 3-5; 1 = adjacent but not core |
| Buyer title match | 5 = CTO / VP Eng / SVP Eng; 3 = Head of Platform / Head of Infra / Director Eng; 0 = non-technical persona |

## 5. SIGNAL SOURCES

| Public Data Point | Example Sources | Maps To ICP Criteria | What To Look For |
|---|---|---|---|
| AI and platform job postings | Greenhouse, Lever, company careers page, LinkedIn Jobs | AI hiring velocity, inference complexity, urgency | Titles like `ML Platform Engineer`, `Inference Engineer`, `AI Infrastructure`, `RAG`, `LLM`, `GPU`, `evaluation`, `observability` |
| Company engineering blog and architecture talks | Company blog, conference agendas, YouTube talks, speaker bios | AI-in-production evidence, observability maturity, trigger events | Mentions of production copilots, latency work, routing, caching, model migration, incident learnings |
| GitHub org activity and repository signals | GitHub repos, Pulse, traffic, topics, commit graphs | AI stack evidence, observability maturity, engineering sophistication | Repos referencing `vllm`, `langchain`, `opentelemetry`, `ray`, `kserve`, `triton`, or active infra work |
| Website tech detection | BuiltWith, Wappalyzer | AI stack evidence, cloud/tooling readiness | Frontend-visible signals plus supporting tags from analytics, cloud, chatbot, or developer tooling footprints; treat as directional, not definitive |
| Funding databases and company announcements | Crunchbase, company newsroom, investor blog, SEC filings | Funding stage, funding recency, ARR pressure, urgency | Recent rounds, acquisitions, growth plans, AI expansion language, board-level efficiency messaging |
| Product pages and pricing pages | Company website, docs, changelog | Monetization pressure, AI-in-production evidence | AI features sold to customers, premium AI tiers, usage-based pricing, enterprise AI messaging |
| Cloud/provider case studies | AWS, Google Cloud, Microsoft, Datadog, LangChain customer stories | AI stack evidence, observability maturity, scale | Named references to Bedrock, Vertex AI, Azure OpenAI, LLM observability, tracing, or production deployments |
| Status pages, postmortems, and trust centers | Public status page, incident writeups, trust center | Reliability urgency, maturity, buyer pain | AI outage language, degraded response times, incident frequency, customer-facing reliability commitments |
| Leadership and speaker profiles | LinkedIn, company leadership page, conference speaker pages | Buyer title match, strategic priority | CTO / VP Eng visibility in AI infra, platform, reliability, or FinOps conversations |

### Source-to-Criterion Mapping Summary

| ICP Criterion | Best Public Sources |
|---|---|
| AI-in-production stack evidence | Engineering blog, GitHub, BuiltWith/Wappalyzer, cloud case studies, product docs |
| Inference scale and complexity | Job postings, engineering talks, architecture posts, GitHub |
| AI observability and reliability maturity | Engineering blog, docs, GitHub, Datadog/LangSmith/OpenTelemetry references |
| AI hiring velocity | Greenhouse, Lever, careers page, LinkedIn Jobs |
| Company headcount fit | LinkedIn company profile, Crunchbase, Apollo, company about page |
| ARR and monetization pressure | Pricing pages, investor updates, SEC filings, analyst coverage |
| Funding stage and recency | Crunchbase, company newsroom, funding announcements |
| Industry fit | Company website, Crunchbase category, LinkedIn description |
| Buyer title match | LinkedIn, leadership pages, speaker directories |

