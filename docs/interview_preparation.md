# Project 07 — Interview Preparation & Statistical Defense

**Project:** Customer Support Hypothesis Testing & Operational Improvement  
**Disclosure:** The company, intervention and data are **synthetic**. This is a before/after analysis with **no randomized or contemporaneous control group**.

## 60–90-second interview explanation

> “I evaluated whether a simulated customer-support training program coincided with better performance. The dataset contains 4,150 tickets across 45 agents and three teams, split into before and after periods. I audited all records and compared first-response speed, SLA compliance, customer satisfaction, resolution time, and ticket complexity. Overall first response fell by 5.57%, but average resolution time rose by 4.20 minutes. For inference I aggregated tickets to one mean response per agent per period, then used a paired t-test. It estimated an average improvement of 0.82 minutes, but p was 0.067 and the 95% confidence interval included zero. A one-way ANOVA of agent improvements across teams was also nonsignificant, with p of 0.174. One Technical agent was an influential outlier, so I reported a sensitivity analysis without replacing the 45-agent primary test. I recommended monitored continuation, prioritizing high-priority SLA breaches and Technical Support, and a future controlled evaluation. My main lesson was to distinguish descriptive improvement, statistical uncertainty, and causal proof.”

## Questions and strong answers

### 1. What was the business problem?
Customer service leadership wanted faster first responses without deteriorating SLA compliance, resolution quality or customer satisfaction. The deliverable was an evidence-based recommendation about a proposed training rollout.

### 2. What is an agent? What is the dataset grain?
An agent is a **human support employee**; `AGT028` is a staff identifier, not an AI agent. Each CSV row is one ticket. The CSV has 4,150 tickets, 45 agents, and three teams with 15 agents each.

### 3. What was the intervention?
A simulated training program emphasizing prompt responses, ticket priority, routing and communication. It was not an intervention performed on real people.

### 4. How is this different from Project 06 A/B testing?
A/B testing normally compares randomized treatment and control groups contemporaneously. Here the **same agents** were measured before and after, with no control group. Seasonal changes, ticket complexity or staffing can confound the association.

### 5. Why did you not pair individual tickets?
Tickets were different interactions across periods. Pairing unrelated tickets would invent matches and mishandle dependence. I aggregated to **one mean per agent per period**, yielding 45 valid matched pairs.

### 6. Why use a paired t-test?
Each agent has a before and after measurement. The paired test evaluates whether the **mean of within-agent changes** differs from zero, controlling for stable differences in agents' baselines better than an unpaired comparison.

### 7. What is the paired difference and its sign?
`improvement = mean_before - mean_after`. A **positive** value indicates faster responses after training. The mean improvement was **+0.8186 minutes**.

### 8. Explain the paired t-statistic manually.
`d_bar = 0.8186`, `s_d = 2.9277`, `n = 45`, so `SE = 2.9277/sqrt(45) ≈ 0.4364`. Then `t = 0.8186/0.4364 ≈ 1.8757` with `df = 44`. SciPy returned the same statistic.

### 9. Interpret the p-value of 0.0673.
Under the zero-population-mean-change hypothesis and test assumptions, a t-statistic at least this extreme (in either direction) would be observed about 6.73% of the time. At alpha 0.05, **do not reject** the null. It is **not** the probability the null is true, and does not prove zero improvement.

### 10. Interpret the 95% confidence interval.
For the population mean of agent-level improvement, the estimated 95% interval was **−0.0610 to +1.6982 minutes**. It includes zero, hence the observed positive mean has nontrivial uncertainty. It is not a statement that 95% of individual agents fall inside this range.

### 11. What is Cohen's paired dz = 0.2796?
It is mean paired improvement divided by the standard deviation of paired differences: `0.8186/2.9277`. It is a standardized paired effect estimate, not the percentage reduction in average response time.

### 12. What were the normality and outlier caveats?
Shapiro–Wilk on the 45 differences gave **p = 0.0056**, suggesting departures from normality. One unusually negative improvement was AGT028 at **−10.2423 min**. With n=45 the t-test can tolerate moderate deviations but a large outlier can influence it; I disclosed both issues.

### 13. Why is the p-value 0.0054 when you exclude AGT028?
Excluding AGT028 increased the estimated improvement from **0.8186 to 1.0700 min**. That **exploratory sensitivity** demonstrates influential data; it does **not** justify excluding a valid agent from the primary analysis or declaring success using the smaller p-value.

### 14. Why use one-way ANOVA?
To compare mean agent-level **improvement** across Billing, General and Technical—three independent groups of agents. Repeating many pairwise t-tests would increase multiple-testing risk.

### 15. Explain the F-statistic and the ANOVA result.
`F = MS_between / MS_within = 15.0824/8.2614 = 1.8256`, with df `(2,42)` and **p = 0.1737**. The data do not establish differences among the three population team mean improvements. It does **not** mean every team performs identically.

### 16. What does eta-squared = 0.08 mean?
Approximately 8% of observed variance in agent-level improvements in this sample is associated with team membership. It is a descriptive model effect size, **not** a causal impact of team or training.

### 17. What are Levene and Welch ANOVA?
Levene tests whether group variances differ; here **p = 0.8681**, so we did not detect unequal variances. Welch ANOVA relaxes the equal-variance assumption; **p = 0.2009**, also nonsignificant. Neither proves normality or fixes outliers.

### 18. Why no Tukey HSD?
The classical omnibus ANOVA was nonsignificant, and we had no prespecified pairwise hypotheses warranting additional multiplicity-controlled testing. If specific team contrasts were a planned confirmatory goal, choose an appropriate procedure based on the variance and distribution assumptions; don't perform tests merely to obtain significance.

### 19. What happened to the Technical team and AGT028?
Technical mean agent-level improvement was **−0.1396 min** and after-period team SLA **64.77%**. AGT028's mean first response increased **17.31 to 27.55 min**, while the share of high-priority tickets rose **18.00% to 38.46%** and complex tickets **14.00% to 38.46%**. Increased case difficulty is a plausible explanation, not confirmed causality; the outlier remains included in primary analysis.

### 20. Was customer satisfaction improved?
Among respondents, the share with a 4/5 rating increased **70.30% to 75.42%**. But survey response rate fell **78.34% to 76.71%**, so selection bias is possible. We didn't claim an independent ticket-level chi-square test because tickets share agents and survey participation is selective.

### 21. Did SLA improve across teams?
Overall SLA increased **75.02% to 76.14%**. Billing improved **75.04% to 80.95%**, while General declined **85.41% to 82.40%** and Technical **65.42% to 64.77%**. SLA depends on ticket priority, so means and service compliance can move in opposite directions.

### 22. Why did resolution time increase despite faster first response?
The overall mean resolution increased **124.85 to 129.05 min**, and complex-ticket share rose **20.88% to 27.76%**. Case-mix changes might help explain the aggregate pattern. We cannot conclude training increased resolution time without a stronger, adjusted design.

### 23. How did you estimate operational impact?
A scenario applied a **0.84-minute** ticket-weighted response reduction to 2,100 after-period tickets: around **1,764 aggregate ticket waiting-minutes (29.4 waiting-hours)** under comparable-case assumptions. This is **not employee-hours saved**. The report's monetary example is explicitly hypothetical and must never be marketed as realized savings.

### 24. What did you recommend?
Continue training conditionally, investigate high-priority response breaches and Technical Support routing, protect resolution and satisfaction, and use case-mix-adjusted monitoring. Seek a contemporaneous control group or staggered rollout before causal claims or indiscriminate expansion.

### 25. Why use Python, SciPy, statsmodels and Matplotlib?
Pandas: cleaning, groupby and paired-agent table; NumPy: numeric arithmetic; SciPy: paired t, Shapiro–Wilk, Levene, classical ANOVA and confidence interval; statsmodels: Welch ANOVA; Matplotlib: five interpretable charts; Jupyter: reproducible reasoning and outputs.

### 26. Where is the AI in this project?
There is **no LLM or machine-learning model in this project**. Its distinct value is statistical inference and decision quality. AI tools can assist with drafting, code review or investigation, but statistical methods and validation should be credited accurately. The user's other portfolio projects separately demonstrate AI workflows.

### 27. How would you improve this study?
Collect more comparable periods, preregister the primary KPI and minimum practical effect, use contemporaneous control or staggered rollout, capture covariates and staffing/routing changes, handle agent/team clustering explicitly where necessary, examine adjusted estimates, and assess persistence and costs using real operational data.

## Interview traps to avoid

- Do **not** say “training caused a 5.57% improvement.” Say the *observed post-training period* had lower mean first-response times.
- Do **not** say “p > 0.05 proves no effect.” Say evidence was inconclusive at alpha 0.05.
- Do **not** use the 44-agent sensitivity p = 0.0054 as the main result.
- Do **not** infer that two teams are statistically different just because their descriptive means differ.
- Do **not** claim customers universally became more satisfied when survey participation changed.
- Do **not** count aggregate customer waiting-time reduction as labor savings.
- Do **not** imply these simulated records are real operational evidence.

## Memorize these eight numbers

| Statistic | Value |
|---|---:|
| Tickets | 4,150 |
| Matched agents | 45 |
| Ticket-level response reduction | 5.57% |
| Mean paired improvement | 0.8186 minutes |
| Paired t-test p-value | 0.0673 |
| Paired 95% CI | [−0.0610, 1.6982] minutes |
| Classical ANOVA p-value | 0.1737 |
| High-priority after-period SLA | 55.35% |

**Evidence source:** Notebook, `output/statistical_results.csv`, and `docs/executive_decision_report.md`.
