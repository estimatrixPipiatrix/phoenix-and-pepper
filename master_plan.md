# Phoenix et Piper — Master Plan

## The Company

Phoenix et Piper is a Roman trading company set in a world where classical sources are literally true — Pliny's *Natural History* is a field manual, Ovid's *Metamorphoses* is recent history, the gods intervene, and the monsters are real.

Two partners founded it in Ostia: one dealing in rare naturalia (phoenix ash, basilisk venom, lodestones), the other in commodities (pepper, garum, silphium, Tyrian purple). They merged because they kept using the same ships.

Two cargo classes define the business:

- **Phoenix-class:** Rare, dangerous, mythological. High margin, high risk, special handling.
- **Pepper-class:** Bulk commodities and spices. Predictable demand, tight margins.

The entire business is about managing the tension between these two sides.

---

## Phase 0 — Founding (Ostia, One Port)

**Story:** Two partners, a warehouse, three ships, a handful of Italian coastal routes. Manual record-keeping.

**Core decision:** What should each ship carry on its next voyage?

**Supporting decisions:** Which orders to fulfill vs. delay; how to allocate cargo space; whether each voyage is profitable.

**Build:**

- Public GitHub repo from day one
- Docker Compose stack (Postgres + Metabase)
- Python project managed with `uv`
- Postgres schema: ships, cargo, routes, customers, orders
- Synthetic data generator (Python "world simulator")
- Unit tests (`pytest`) from the start
- GitHub CI/CD pipeline
- Simple Metabase dashboards: revenue, cargo mix, ship utilization

**Skills:** Postgres, data modeling, Python, Metabase, Docker/Compose, pytest, CI/CD.

**Business concepts:** Revenue/cost/margin, utilization rate, inventory tracking, KPIs and dashboards.

**Blog ideas:** "I started a fake Roman trading company to learn BI" · "Designing a database for mythological cargo"

**Dashboard question:** *What should we load onto Ship III tomorrow?*

---

## Phase 1 — Coastal Expansion (Western Mediterranean)

**Story:** Routes expand to Massilia, Carthago Nova, Gades. More ships, more crew, a competitor appears, and Neptune is displeased.

**Core decision:** Which routes should we operate, and how should ships move through the network?

**Supporting decisions:** Optimal shipment paths; whether to accept risky routes (divine hazards, seasonal winds, monster sightings); where to add or cut capacity.

**Build:**

- Graph model of the trade network (ports = nodes, routes = edges)
- Route optimization with constraints
- Demand forecasting via Markov processes
- Richer Metabase dashboards (route performance, port analytics)
- First Dash/Plotly app: interactive route planner with map

**Skills:** NetworkX, Graphviz, Markov processes, Dash + Plotly, geospatial thinking.

**Business concepts:** Route/network optimization, demand forecasting, competitive analysis, scenario planning.

**Blog ideas:** "Graph-based route optimization for a Roman shipping company" · "Forecasting demand for basilisk venom with Markov chains" · "Building an interactive trade route planner in Dash"

**Dashboard question:** *Should we route through Massilia or avoid it this week?*

---

## Phase 2 — The Platform (Customer-Facing System)

**Story:** Customers want to place orders directly. You build a portal. Suddenly you have user behavior data — who's browsing, buying, or vanishing.

**Core decision:** Which customers should we invest in keeping, and how?

**Supporting decisions:** Who is likely to churn; which segments are most valuable; where customers drop off in the funnel.

**Build:**

- Simulated user behavior data (sessions, orders, browsing)
- Customer segmentation via clustering
- Churn prediction model
- Engagement funnel analysis
- Metabase: cohort analysis, retention curves
- Dash app: customer health dashboard

**Skills:** Agent-based modeling, graph analytics (customer-product-order graphs), ML classification (scikit-learn), cohort analysis.

**Business concepts:** Customer lifecycle, churn/retention, funnel analysis, segmentation, product analytics.

**Blog ideas:** "Simulating customer behavior with agent-based models" · "Which Roman merchants are about to churn? A Bayesian approach" · "Building a customer health dashboard for a mythological supply chain"

**Dashboard question:** *Which merchants do we need to save right now?*

---

## Phase 3 — Security and Fraud (The Underworld Arrives)

**Story:** Pirates (some cursed), fraudulent orders, a warehouse theft ring, and someone is smuggling Medusa heads through your supply chain. You hire mercenaries — and must decide how many, where to deploy them, and whether they're worth the cost.

**Core decision:** Where should we deploy protection and scrutiny to minimize loss?

**Supporting decisions:** Which shipments/customers are high-risk; which transactions to flag; mercenary allocation.

**Build:**

- Transaction anomaly detection
- Network-based fraud detection on the transaction graph
- Bayesian network for risk scoring
- Automated alerting (Metabase/Dash)
- Incident response workflow (state machine / Markov process)
- Mercenary deployment optimization (resource allocation under threat uncertainty)

**Skills:** Anomaly detection (Markov + ML), Bayesian networks, graph-based fraud detection, event-driven architecture.

**Business concepts:** Fraud detection, risk scoring, monitoring/alerting, incident response, compliance.

**Blog ideas:** "Detecting smugglers in a Roman trade network with graph anomaly detection" · "Bayesian risk scoring for mythological cargo" · "When your anomaly detector catches a literal monster"

**Dashboard question:** *Which shipment is most likely to be compromised?*

---

## Phase 4 — The Empire (Scale and Infrastructure)

**Story:** Dozens of ports, hundreds of ships, thousands of customers across the entire Mediterranean. The data infrastructure itself becomes a challenge.

**Core decision:** How does the organization make decisions reliably at scale?

**Supporting decisions:** Which pipelines are trusted; what metrics drive decisions across teams; how to automate recurring decisions.

**Build:**

- Kubernetes (graduating from Docker Compose)
- `dbt` for data transformations
- GitHub CI/CD for orchestrating data workflows (scheduled runs, data validation)
- Pydantic AI agent for natural-language data queries
- MBSE: system models visualized with NetworkX + Graphviz

**Skills:** Data engineering (ETL/ELT), Kubernetes, Pydantic/Pydantic AI, MBSE, infrastructure-as-code.

**Business concepts:** Data engineering/pipelines, data governance, enterprise architecture, decision intelligence as formal practice.

**Blog ideas:** "Scaling a Roman trading empire with Kubernetes and dbt" · "Building a decision intelligence layer for Phoenix et Piper" · "MBSE and NetworkX"

**Dashboard question:** *Can I trust this decision without manually checking the data?*

---

## Tool Stack (All Free / Open Source)

| Tool | Role | Phase |
|------|------|-------|
| Git + GitHub | Version control, public repo, CI/CD | 0 |
| Docker / Compose | Containerization, reproducible environments | 0 |
| uv | Python project/dependency management | 0 |
| pytest | Unit testing | 0 |
| Postgres | Core database | 0 |
| Python | Everything — data gen, modeling, analysis | 0 |
| Metabase | BI dashboards, SQL exploration | 0 |
| NetworkX | Graph analytics | 1 |
| Graphviz | Graph visualization | 1 |
| Dash + Plotly | Interactive visualizations and apps | 1 |
| scikit-learn | ML models (churn, anomaly, classification) | 2 |
| dbt | Data transformation | 4 |
| Kubernetes | Orchestration | 4 |
| Pydantic AI | AI-powered data agent | 4 |
