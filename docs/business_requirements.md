# Business Requirements Document — Project 07
**Customer Support Hypothesis Testing & Operational Improvement**  
**Version:** 1.0 | **Status:** Execution-ready baseline | **Data:** Synthetic; not a real-company evaluation

## Background and problem
A fictional customer support organization runs Billing, Technical, and General teams. Management reports slow initial responses, inconsistent SLA performance, and uneven team results. An organization-wide training intervention aims to improve prioritization, routing, and customer communication. Management needs a credible assessment of what changed after training without incorrectly attributing observed changes to the program.

## Objectives and business decision
Measure first-response-time change; test whether average **agent-level** response times differ before versus after training; compare improvements across teams; and check that customer satisfaction, resolution performance, and SLA compliance remain acceptable. Decide whether to continue, refine, or further evaluate the intervention. **Before/after association does not prove causality.**

## Stakeholders
**Head of Support:** sponsor and rollout decision. **Operations Manager:** KPIs and staffing. **Team Leads:** team follow-up. **Training & Quality Manager:** coaching and quality. **Business Analyst:** auditable statistical analysis and recommendations.

## Business questions and KPIs
Did response times decrease, by how many minutes and what percentage? Is the average agent-level change statistically distinguishable from zero? Do improvement patterns differ across teams? Did ticket volumes, priority, or complexity change? Did CSAT, SLA compliance, or resolution quality deteriorate?

**Primary KPI:** first meaningful response time (minutes). Report ticket-weighted operational means separately from equally weighted agent-level means. **Secondary KPIs:** response-time median, SLA compliance (% meeting ticket target), CSAT mean (1–5) and survey response rate, resolution time, ticket volumes, and team/priority/complexity mix.

## Dataset requirements
Exactly **one** `data/support_tickets.csv`; one row per ticket, approximately 4,150 simulated tickets across 45 agents, three stable teams, and two 45-day windows. Required fields: ticket ID/date, period, agent, team, category, priority, complexity, response time, resolution time, optional CSAT rating, SLA target, and training-completed flag. Reproducible generator with fixed seed, valid values, unique IDs, and at least 25 tickets per agent in each period. Simulation assumes different team-level training effects, variation including some deterioration, shifts in ticket mix, and CSAT nonresponse. These are **assumptions**, not factual findings.

## Statistical evaluation
**Primary:** two-sided paired t-test on one before and one after mean per matched agent; calculate mean *after − before* difference, t-statistic, degrees of freedom, p-value, 95% confidence interval, effect size, and assumption checks. **Secondary:** one-way ANOVA of agent-level *before − after* improvement across three teams; perform post-hoc comparisons only if justified. CSAT and SLA remain descriptive guardrails unless an additional valid test is warranted.

## Expected deliverables
Usable starter ZIP; one-page BRD; reproducible source CSV and generator; validated Jupyter notebook; four or five purposeful charts; saved statistical results; evidence-backed executive report with operational scenarios, prioritized actions, owners, and success measures; documented GitHub repository.

## Acceptance criteria
1. Full one-pass data audit; correct matching and stable team assignments; missing CSAT never treated as a low rating.
2. Correct analysis units, estimands, test assumptions, confidence intervals, effect sizes, and reproducible results.
3. Clear distinction between observed association and causal effects; no unsupported claims of labor-hour savings.
4. Guardrail and case-mix investigation, quantified recommendations, full notebook rerun, and clean GitHub publication.

**Out of scope:** Power BI, ML, LLM tools, cloud services, and unsupported causal claims.
