# Customer Support Training — Statistical Evaluation & Executive Decision Report

**Project:** Project 07 — Customer Support Hypothesis Testing & Operational Improvement  
**Report type:** Management decision memorandum  
**Data:** Synthetic, reproducible support-ticket simulation; no real customers or employees  
**Observation periods:** Before: 1 July–14 August 2026; After: 15 August–28 September 2026  
**Unit of primary statistical analysis:** Human support agent (one before-period and one after-period average per agent)  
**Status:** Draft based on verified notebook outputs supplied for this project; final notebook QA and GitHub publication pending

> **Evidence standard:** All descriptive and statistical findings below are based on this *simulated* dataset and the analysis outputs. They are not evidence that a real company's training program worked. A before/after design with no contemporaneous control group does not support a definitive causal conclusion.

## A. Executive summary and recommended decision

**Recommended decision: Continue the simulated training framework on a monitored, conditional basis; do not claim statistically established or causal effectiveness, and do not expand it indiscriminately.** Prioritize a review of Technical Support and high-priority SLA performance; monitor a matched follow-up period, then evaluate a controlled rollout where feasible.

The dataset includes **4,150 tickets** handled by **45 agents across three teams**—2,050 tickets before training and 2,100 after training. Ticket-weighted mean first-response time fell from **15.06 to 14.22 minutes** (approximately **0.84 minutes or 5.57%**). SLA compliance improved from **75.02% to 76.14%** (**+1.12 percentage points**), and the share of satisfied customers *among survey respondents* rose from **70.30% to 75.42%** (**+5.12 percentage points**). However, mean ticket resolution time increased from **124.85 to 129.05 minutes** (**+4.20 minutes**). Survey participation fell from **78.34% to 76.71%**.

The **paired agent-level t-test** estimated a mean before-minus-after improvement of **0.8186 minutes** across 45 matched agents (t(44) = **1.8757**, two-sided **p = 0.0673**, 95% CI **[−0.0610, 1.6982]** minutes, paired Cohen's *d*<sub>z</sub> = **0.2796**). The test **did not reject the zero-change null hypothesis at α = 0.05**. This is inconclusive evidence, not proof of no benefit. An exploratory sensitivity check that omitted unusual agent AGT028 gave a larger mean improvement (**1.0700 minutes**, p = **0.0054**); this does **not** supersede the all-agent primary result.

The team-comparison **one-way ANOVA** was also nonsignificant (**F(2,42) = 1.8256, p = 0.1737**, η² = **0.0800**); Welch's ANOVA agreed (**F ≈ 1.7034, p = 0.2009**). Billing improved most descriptively, but statistical evidence does not establish a population mean difference among the teams. Because the primary omnibus result was nonsignificant and the improvement distributions have caveats, no automatic Tukey HSD post-hoc claims are warranted.

**Management implication:** Descriptive gains are encouraging, yet the unresolved Technical Support outlier, worsening resolution-time averages, modest overall SLA movement and significant case-mix shift warrant targeted investigation and continued measurement rather than an unqualified success declaration.

## B. Business question, operating model and evaluation design

The hypothetical business employs **45 human customer-support agents**: 15 each in **Billing**, **General**, and **Technical** support. A *ticket* is one customer inquiry assigned to an agent. Response time represents the time until the first meaningful response; resolution time represents the time to solve the issue. A simulated support-training intervention emphasized timely replies, prioritization, routing and communication. The same agents were observed in both periods.

This is **an observational before/after comparison**, not an A/B test. Team-level and period-level ticket composition can change. Individual tickets before training cannot be paired to unrelated tickets afterward; instead, each agent's average response time was computed within each period, generating 45 matched pairs. The paired test treats each agent equally. Overall descriptive ticket averages instead weight agents by their number of tickets and are **not identical estimands**.

Primary decision question: *Is there sufficient evidence of a change in mean agent response time after training?* Secondary question: *Is average agent-level change different across support teams?* Operational guardrails: SLA achievement, satisfaction, resolution time, ticket priority/complexity and survey response coverage.

## C. Operational performance scorecard

| KPI | Before | After | Observed change |
|---|---:|---:|---:|
| Tickets | 2,050 | 2,100 | +50 (+2.44%) |
| Distinct agents | 45 | 45 | Unchanged |
| Ticket-weighted mean response time | 15.06 min | 14.22 min | −0.84 min (−5.57%) |
| Median response time | 12.65 min | 11.94 min | −0.71 min |
| Mean resolution time | 124.85 min | 129.05 min | +4.20 min |
| Median resolution time | 105.06 min | 109.61 min | +4.55 min |
| SLA-compliant tickets | 1,538 | 1,599 | +61 |
| SLA compliance | 75.02% | 76.14% | +1.12 pp |
| Tickets missing SLA | 512 | 501 | −11 |
| Recorded CSAT responses | 1,606 | 1,611 | +5 |
| CSAT survey response rate | 78.34% | 76.71% | −1.63 pp |
| Mean recorded CSAT | 3.97/5 | 4.04/5 | +0.07 points |
| Respondents rating 4 or 5 | 1,129 | 1,215 | +86 |
| Satisfied share of respondents | 70.30% | 75.42% | +5.12 pp |
| High-priority ticket share | 21.71% | 28.05% | +6.34 pp |
| Complex-ticket share | 20.88% | 27.76% | +6.88 pp |

**Denominators matter.** Overall SLA compliance = compliant tickets ÷ all tickets. Satisfaction share = ratings of 4 or 5 ÷ *tickets with a recorded rating*, not all tickets. Response coverage = recorded ratings ÷ all tickets. Percentage-point differences must not be confused with relative percentage changes.

**Interpretation:** First-response waiting time fell while resolution time rose. The higher proportion of high-priority and complex tickets in the after period may help explain parts of the workload and SLA pattern. Neither this possible explanation nor the intervention's causal effect has been established. Satisfaction trends are conditional on survey participation; nonrespondents' satisfaction is unknown.

## D. Statistical evaluation of the training-period change

### D1. Primary paired t-test — 45 agents

For agent *i*, define **dᵢ = mean response time before − mean response time after**. Positive *dᵢ* indicates faster post-period responses. The hypothesis test was two-sided: **H₀: μd = 0** versus **H₁: μd ≠ 0**.

| Quantity | Result |
|---|---:|
| Matched agents | 45 |
| Agent-weighted mean before | 15.01 min (rounded) |
| Agent-weighted mean after | 14.20 min (rounded) |
| Mean paired improvement | +0.8186 min |
| Median paired improvement | +0.710 min |
| SD of paired differences | 2.9277 min |
| SE of mean paired difference | 0.4364 min |
| t statistic / df | 1.8757 / 44 |
| Two-sided p-value | 0.0673 |
| 95% CI of mean improvement | [−0.0610, 1.6982] min |
| Paired Cohen's d_z | 0.2796 |
| Agents improved / deteriorated / unchanged | 27 / 18 / 0 |

A useful manual verification is **t = 0.8186 ÷ (2.9277 / √45) ≈ 1.8757**, consistent with SciPy's paired t-test. Because **p > 0.05** and the 95% CI crosses zero, the null was not rejected. The observed positive mean is promising but uncertain; the interval permits a small deterioration as well as a larger improvement.

**Assumption caution:** A Shapiro–Wilk normality diagnostic on the 45 agent differences gave **W = 0.9236, p = 0.0056**. One unusually negative agent difference was flagged. The paired t-test can be moderately robust with 45 observations, but the distributional caveat and outlier influence must be disclosed. Shared operating conditions may also introduce dependence between agents; this is not diagnosed by Shapiro–Wilk.

### D2. AGT028 — sensitivity, not deletion

The most unusual observation was **AGT028, Technical Support**, with a mean response-time change of **+10.24 minutes slower** (equivalently **−10.2423 minutes improvement**). A sensitivity calculation *excluding* this agent, without altering the primary data, yielded:

| Estimate | All 45 agents (primary) | 44 agents excluding AGT028 (sensitivity) |
|---|---:|---:|
| Mean improvement | 0.8186 min | 1.0700 min |
| t statistic | 1.8757 | 2.9317 |
| p-value | 0.0673 | 0.0054 |
| 95% CI | [−0.0610, 1.6982] | [0.3340, 1.8060] |

The change in significance shows the result is **sensitive to AGT028**. Excluding a valid employee because their outcome is unfavorable would bias the analysis; all 45 agents remain in the primary estimate. The sensitivity result is a diagnostic and should not be promoted as proof that training worked.

### D3. Team-level one-way ANOVA

Each of the 45 agents contributes one improvement value. A classical one-way ANOVA tested equal population mean improvements for Billing, General and Technical:

| ANOVA component | Result |
|---|---:|
| Between-team sum of squares | 30.1649 |
| Within-team sum of squares | 346.9801 |
| Between / within degrees of freedom | 2 / 42 |
| Between / within mean squares | 15.0824 / 8.2614 |
| F statistic | 1.8256 |
| p-value | 0.1737 |
| Eta-squared, η² | 0.0800 |
| Welch F | 1.7034 |
| Welch p-value | 0.2009 |
| Levene variance-test p-value | 0.8681 |

**Decision:** Do not reject equality of team mean improvements at α = 0.05. η² = 0.08 describes the observed share of improvement variability associated with team grouping *in this sample*, not a causal attribution. Welch's ANOVA does not overturn the inference. Levene's result does not prove equal variances.

The Technical group showed evidence against normality (Shapiro–Wilk **p = 0.0140**). After omitting AGT028 in an exploratory ANOVA sensitivity check, Technical mean improvement became **+0.5820 minutes**, classical ANOVA **p = 0.2995**, Welch **p = 0.3223**, and Technical Shapiro–Wilk remained low (**p = 0.0100**). Therefore, the team-level significance conclusion **remains nonsignificant** with or without that agent, and the normality concern cannot be attributed solely to the one observation.

**Post-hoc decision:** No automatic Tukey HSD or named pairwise significance claims. If a future confirmatory study identifies a meaningful omnibus difference, follow-up comparisons should be chosen and multiplicity addressed based on their assumptions and objectives.

## E. Team performance investigation

| Team | Tickets before → after | Mean response before → after | Change | SLA before → after | Mean resolution before → after | Satisfied respondents before → after |
|---|---|---|---:|---|---|---|
| Billing | 665 → 740 | 14.83 → 13.09 min | −1.74 min | 75.04% → 80.95% | 117.28 → 122.13 min | 71.24% → 78.15% |
| General | 665 → 676 | 12.57 → 11.82 min | −0.75 min | 85.41% → 82.40% | 96.37 → 97.68 min | 73.95% → 75.69% |
| Technical | 720 → 684 | 17.56 → 17.82 min | +0.26 min | 65.42% → 64.77% | 158.15 → 167.55 min | 66.08% → 72.21% |

**Billing — encouraging but qualified.** Among its 15 agents, **11 improved**, and its agent-weighted mean response-time reduction was **1.8606 minutes**. Its ticket-weighted response time and SLA rate also improved, but resolution time rose **4.85 minutes**. Investigate whether complexity changed or faster acknowledgement was followed by longer case handling.

**General — response/SLA divergence.** Among 15 agents, **10 improved**. Its agent-level mean improvement was **0.7348 minutes**, yet SLA compliance fell **3.01 pp** despite faster average responses. Priority-specific targets, changes in ticket mix, upper-tail delays and service routing should be assessed before assigning a cause.

**Technical — highest apparent operational risk.** Only **6 of 15 agents improved**; mean agent-level change was **−0.1396 minutes**, and ticket-weighted mean response time increased by **0.26 minutes**. The team had the worst after-period SLA rate (**64.77%**) and longest mean resolution time (**167.55 minutes**). This justifies focused operational review even though the ANOVA did not establish statistically significant differences among team means.

### E1. AGT028 deep dive

| AGT028 metric | Before | After |
|---|---:|---:|
| Tickets | 50 | 52 |
| Mean / median response | 17.31 / 12.96 min | 27.55 / 20.52 min |
| 90th-percentile response | 26.30 min | 44.45 min |
| Mean resolution | 142.88 min | 168.35 min |
| SLA compliance | 74.00% | 36.54% |
| High-priority share | 18.00% | 38.46% |
| Complex-ticket share | 14.00% | 38.46% |
| Mean recorded CSAT | 4.05/5 | 3.63/5 |

The agent's median and 90th percentile also deteriorated, so the issue is not visible only in the mean. At the same time, high-priority and complex-ticket shares more than doubled. This is a **plausible case-mix confounder**, not proof of the cause. Review priority/complexity-standardized outcomes, assignment policy, escalations, staffing, and whether there were simultaneous workflow changes. Do not use this synthetic diagnostic to make adverse employee-level judgments.

## F. Priority, complexity and customer-experience guardrails

### F1. Ticket-priority performance

| Priority | Before tickets | After tickets | Before mean response | After mean response | SLA before | SLA after |
|---|---:|---:|---:|---:|---:|---:|
| High | 445 | 589 | 11.11 min | 11.07 min | 51.01% | 55.35% |
| Medium | 995 | 970 | 14.70 min | 14.31 min | 77.49% | 81.75% |
| Low | 610 | 541 | 18.52 min | 17.49 min | 88.52% | 88.72% |

**High-priority SLA is the most actionable service gap.** After training, approximately **263 of 589 high-priority tickets** missed their targets (**44.65%**). Before, about **218 of 445** missed. The *rate* improved **4.34 pp**, but the absolute count of high-priority breaches rose by about **45** because high-priority volume increased markedly. The target for high-priority tickets is stricter than for medium and low priority; mean response time alone cannot establish SLA compliance.

### F2. Ticket-complexity performance

| Complexity | Before tickets | After tickets | Before mean response | After mean response | Mean resolution before → after | SLA before → after |
|---|---:|---:|---:|---:|---|---|
| Complex | 428 | 583 | 19.99 min | 18.78 min | 166.22 → 165.57 min | 53.27% → 59.18% |
| Moderate | 924 | 866 | 14.76 min | 13.73 min | 123.96 → 125.71 min | 76.41% → 78.98% |
| Simple | 698 | 651 | 12.42 min | 10.79 min | 100.66 → 100.79 min | 86.53% → 87.56% |

Within each complexity category, mean first-response time decreased descriptively, while the **overall case mix shifted toward more complex tickets**. This suggests that a stratified or case-mix-standardized comparison could be informative; it does not by itself identify a causal mechanism. Average resolution time among complex tickets decreased slightly, even though the overall mean increased, so composition must be taken seriously.

### F3. Satisfaction interpretation and missing responses

Recorded satisfaction increased from **1,129 / 1,606 = 70.30%** to **1,215 / 1,611 = 75.42%**. However, nonresponse was **444 tickets before** and **489 after**, with the response rate declining **1.63 pp**. Respondents may not be representative of all customers; the result is not a causal or population-wide satisfaction claim. No separate chi-square significance claim is made because ticket responses may be correlated within agents and customer participation is selective.

## G. Quantified operational implications and scenarios

**G1. Observed SLA burden.** The after period contained **501 SLA-breaching tickets** out of 2,100, compared with **512 out of 2,050** before. The after-period breach *rate* was lower, but **501 breaches per 45-day reporting period** remain a material customer-service concern.

**G2. High-priority improvement scenario, not forecast.** Holding after-period high-priority volume at **589 tickets**, increasing high-priority SLA compliance from **55.35% to 70.00%** would correspond to roughly **86 additional timely first responses** (589 × [0.70 − 0.5535] ≈ 86). This is a *proposed operational target*, not a predicted impact of training.

**G3. Customer waiting-time-equivalent scenario, not payroll savings.** Applying the observed **0.84-minute** ticket-weighted reduction to the **2,100 after-period tickets**, under the hypothetical assumption of otherwise comparable tickets, gives **2,100 × 0.84 = 1,764 minutes**, or approximately **29.4 aggregate ticket waiting-hours**. This does **not** represent 29.4 employee-hours saved: customer waiting time and agent active working time are different, and waiting intervals can overlap.

**G4. Financial-value framework (explicitly hypothetical).** A valid cost estimate would require verified escalation probabilities, cost per escalation, staffing utilization and attributable change. For illustration *only*, if 86 more high-priority tickets meeting SLA prevented an escalation for **10%** of those tickets at **₹500** of avoidable cost each, the arithmetic would be **86 × 10% × ₹500 = ₹4,300 per comparable period**. None of the assumed escalation relationship, cost or causal effect is observed in this dataset; **₹4,300 is not measured, forecast or realized savings**. Exclude it from résumé claims unless supported by operational data.

## H. Prioritized management recommendations

| Priority | Action and rationale | Suggested owner | Timing | Proposed success measure |
|---|---|---|---|---|
| P1 | **High-priority SLA triage:** review queue routing, initial response coverage and breaches; 44.65% of after-period high-priority tickets missed target | Support Operations Manager / Routing Lead | Within 14 days | High-priority SLA ≥70% in the next comparable period; review breach count weekly |
| P1 | **Technical Support diagnostic:** examine case mix, coverage and delayed response tails; worst current team SLA (64.77%) and longest resolution time (167.55 min) | Technical Support Lead | Within 21 days | Technical SLA ≥70%; monitor mean and 90th-percentile response, adjusted by case mix |
| P1 | **Review AGT028 non-punitively:** compare assignment changes and complex/high-priority tickets before and after; document findings without deleting observation | Technical Team Lead / Quality Analyst | Within 14 days | Root-cause checklist completed; targeted routing/coaching trial documented |
| P2 | **Protect resolution quality:** faster initial response coincided with +4.20 min average resolution time | Customer Experience Manager | Within 21 days | Case-mix-adjusted resolution time stable or declining; CSAT not deteriorating |
| P2 | **General-team SLA investigation:** response mean improved but SLA declined by 3.01 pp | General Support Lead | Within 21 days | General SLA restored to ≥85% and analyzed by ticket priority |
| P2 | **Strengthen customer-survey coverage:** after-period CSAT response rate was 76.71% | CX Insights Lead | Within 30 days | Survey response rate ≥80%; compare respondents vs nonrespondents on observable ticket attributes |
| P2 | **Evaluate effectiveness with a stronger design:** use a controlled or staggered rollout with comparable teams and preregistered outcomes | Analytics Lead / Training Manager | Plan within 30 days | Defined comparison group, minimum practical effect, sampling plan and guardrails |

Targets and timeframes above are **management proposals**, not statistically derived promises.

## I. Management decision, confidence and monitoring plan

**Decision:** Maintain the training as a controlled operating initiative rather than declare proven success or initiate a broad expansion. Conduct focused high-priority and Technical reviews, improve measurement, and revisit the decision after a new matched reporting window. Where operations permit, implement a contemporaneous comparison group or staggered rollout to distinguish training effects from calendar and case-mix effects.

**Evidence assessment:**

- **High confidence in descriptive calculations conditional on the simulated CSV:** the 12 quality checks passed, date ranges are valid, counts reconcile, and the paired t statistic agrees between manual and SciPy calculations.
- **Limited inferential confidence in an overall mean improvement:** paired p = 0.0673, CI crosses zero, the difference distribution departs from normality and a single agent materially changes the sensitivity result.
- **Limited support for different team mean changes:** classical p = 0.1737 and Welch p = 0.2009; the Technical difference distribution departs from normality. Descriptive performance gaps can still merit operational review.
- **Low confidence in causal attribution or financial savings:** no randomized/contemporaneous control group or observed labor-time, escalation-cost or retention outcomes.

**Next-cycle scorecard:** Compare the following by period, team and priority/complexity: (1) mean/median/p90 first response, (2) SLA met ÷ tickets and breach count, (3) mean/median resolution, (4) CSAT 4–5 ÷ responding tickets, (5) CSAT responses ÷ all tickets, (6) matched-agent mean change with uncertainty, and (7) ticket mix. Use a consistent reporting window, stable KPI definitions, and explicit documented exceptions.

**Decision gates for any expansion:** demonstrable and durable reduction in response time, no unacceptable guardrail deterioration, adequate survey coverage, and a stronger assessment of attributable impact. Do not rely solely on whether an individual p-value crosses 0.05.

## J. Limitations and analytical integrity

1. **Synthetic data:** All company, staff and ticket records were simulated; external real-world generalization is not warranted.
2. **Observational intervention design:** No randomized control, so temporal shifts, seasonal demand, ticket routing or other initiatives may explain changes.
3. **Case-mix shift:** High-priority share rose **6.34 pp** and complex share rose **6.88 pp**. Unadjusted before/after means are not like-for-like case-mix estimates.
4. **Agent-level pairing:** Appropriate to the same 45 agents, but individual tickets differ between periods; other repeated-measures dependencies may remain.
5. **Outlier sensitivity and nonnormality:** Shapiro-Wilk overall **p = 0.0056**; AGT028 strongly influences the paired result, and Technical Shapiro remains below 0.05 even when AGT028 is excluded.
6. **Sample size and uncertainty:** 45 paired agents, 15 per team. A nonsignificant result is not evidence of zero effect.
7. **Uneven ticket loads:** Ticket-weighted mean reduction **0.84 min** and agent-weighted mean reduction **0.8186 min** answer different questions.
8. **CSAT nonresponse:** 933 tickets lacked ratings; survey response rates changed and respondents may differ systematically.
9. **Multiple comparisons:** Follow-up findings and sensitivity analyses are exploratory. The team ANOVA was nonsignificant; automatic pairwise significant claims are unjustified.
10. **Metric-to-money conversion:** First-response waiting time is not agent handle time, and no verified payroll savings or prevented escalations were measured.
11. **Team correlation:** Agents may share managers, schedules or workflows; independence across agent changes is an assumption, not a guaranteed fact.
12. **Data-source QA:** The source CSV had a transient local date-format issue during development. The restored ISO-format CSV passed date and all other audit checks; this fix must remain reproducible on a fresh kernel.

## K. Deliverables and reproduction

**Source CSV:** `data/support_tickets.csv` (4,150 rows; date format `YYYY-MM-DD`).  
**Generator:** `python/generate_data.py` (fixed random seed; reproducible synthetic outcomes).  
**Notebook:** `notebooks/support_training_analysis.ipynb`.  
**Figures:** `output/figures/01_response_time_comparison.png` through `05_customer_experience_guardrails.png`.  
**Requirements:** `requirements.txt`.  
**Primary report:** `docs/executive_decision_report.md` (this document).

Reproducibility checks to complete in final Phase 5: restart kernel and run the notebook top-to-bottom; confirm **12/12 audit PASS**, **45 matched agents**, **t = 1.8757**, **paired p = 0.0673**, **ANOVA F = 1.8256**, **ANOVA p = 0.1737**, all five figures, and that this report and README accurately reflect the notebook outputs. No unreviewed modifications to the simulated data should be used to improve the p-values.

---

**Suggested 60-second executive message:** “We evaluated 4,150 simulated support tickets across 45 agents before and after a training intervention. Mean first-response time declined by 5.57% and satisfaction among survey respondents improved, but resolution time rose and priority/complexity increased. The paired agent-level test estimated a 0.82-minute improvement, yet p = 0.067 and its confidence interval includes zero. Team-level ANOVA also did not establish significant differences. A Technical agent's deterioration strongly influenced the overall paired result and coincided with a much more demanding case mix. We therefore recommend monitored continuation, focused high-priority and Technical reviews, and a stronger controlled evaluation before attributing improvements to training.”
