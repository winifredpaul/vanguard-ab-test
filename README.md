# vanguard-ui-experiment-analysis
# Vanguard A/B Test Analysis — Digital UI Redesign

Evaluating whether Vanguard's redesigned digital interface improved client completion of an online investment process, using exploratory data analysis, KPI measurement, and statistical hypothesis testing.

## Business Context

Vanguard ran an **A/B experiment** to test whether a redesigned digital interface (more intuitive layout, contextual prompts) improved the client experience during an online investment process, compared with the existing interface.

- **Control Group** — used the existing interface
- **Test Group** — used the redesigned interface
- **Experiment window** — 15 March 2017 to 20 June 2017

**Business question:** Did the redesigned interface significantly improve user completion rates and overall customer experience compared with the existing interface — enough to justify a full rollout, both statistically and economically?

## Project Objectives

- Explore and clean the client demographic and behavioural datasets
- Analyse user demographics and navigation behaviour
- Calculate key performance indicators (KPIs) to measure user experience
- Compare Test vs Control performance
- Run hypothesis tests to determine whether observed differences are statistically significant
- Evaluate whether the redesign clears Vanguard's **+5% cost-effectiveness threshold**
- Provide data-driven recommendations for future product improvements

## Data Sources

Three raw datasets, loaded directly from GitHub (raw URLs, no local file paths required):

| File | Description |
|---|---|
| `df_final_demo` | Client demographics — tenure, age, gender, number of accounts, balance, recent call/logon activity |
| `df_final_web_data_pt_1` / `_pt_2` | Clickstream/web activity log — one row per client interaction with the digital process (`start`, `step_1`, `step_2`, `step_3`, `confirm`) |
| `df_final_experiment_clients` | Roster mapping each client to `Test`, `Control`, or no assignment (not part of the experiment) |

These are cleaned, merged, and de-duplicated into two main analysis-ready datasets used throughout the notebook:

- **`clients_df`** (a.k.a. `experiment_final_df`) — one row per client, with demographics, experiment group, and their **furthest step reached** in the funnel. Used for client-level KPIs (completion rate, funnel segmentation, hypothesis tests).
- **`web_events_df`** — one row per event/interaction, labelled with experiment group. Used for event-level KPIs (time per step, backward navigation/error rate).

## Methodology

The notebook is organized into four phases:

1. **Data Collection, Cleaning & Integration** — load, inspect, de-duplicate, standardize column names, merge demographics with the experiment roster and web activity logs, and determine each client's furthest step reached in the funnel.
2. **Exploratory Data Analysis (EDA)** — client demographics (age, gender, tenure, accounts, balance) and engagement behaviour (logons, calls), plus a Test/Control balance check to confirm the randomization was reasonable.
3. **Performance Metrics (KPIs)** — see below.
4. **Statistical Hypothesis Testing** — formal significance testing on the primary KPI, plus effect size and power analysis.

A final **Experiment Evaluation** section reviews the experiment's design quality, duration, and what additional data would strengthen future iterations, and a **Bonus** section adds supplementary analysis (navigation-path comparison, effect size/power, a Streamlit dashboard skeleton, and a Tableau-ready data export).

## KPIs Calculated

The three **primary KPIs** required for the analysis, each computed for Test vs Control:

1. **Completion Rate** — proportion of clients whose furthest step reached is `confirm`.
2. **Time Spent per Step** — median/mean seconds between consecutive events within a visit, with an inspection and exclusion of extreme (>30 min) idle gaps, and a separate sensitivity check on the `confirm` step.
3. **Error Rate (Backward-Transition Rate)** — proportion of step transitions that move backward in the funnel (e.g. `step_3 → step_2`), used as a proxy for user confusion or reconsideration.

The notebook also computes a set of **secondary/segmentation KPIs**, layered on top of the completion-rate metric:

- Step-level funnel drop-off and conversion (KPI 1B)
- Funnel drop-off by step and variation (KPI 4)
- Completion rate by age group (KPI 5), digital engagement/logons (KPI 6), tenure (KPI 9), and balance tier (KPI 10)
- Confirm-step friction score (KPI 7)
- Traffic split / Sample Ratio Mismatch check (KPI 8)

> **Note on scope:** Formal statistical hypothesis testing (z-tests, confidence intervals, effect size, and power analysis) in this notebook is applied **only to the completion-rate KPI**, not to the time-spent or error-rate KPIs, which remain descriptive. See "A Note on the Probability/Statistical Testing Cells" below for why, and what to consider if standardizing this across all KPIs.

## Hypothesis Testing (Phase 3)

Three hypotheses are tested on the completion-rate data:

1. **H1 — Completion rate difference (two-proportion z-test):** Is the Test completion rate different from Control?
   → **Significant.** z = 8.89, p ≈ 5.96 × 10⁻¹⁹. Reject H₀.
2. **H2 — Cost-effectiveness threshold (+5% relative uplift, one-tailed z-test):** Does the Test completion rate exceed Control by more than 5%?
   → **Not statistically confirmed.** Observed uplift is 5.66% (nominally above the 5% bar), but z = 1.04, p = 0.149 — fail to reject H₀.
3. **H3 — Step-level funnel conversion (four two-proportion z-tests with Bonferroni correction, α = 0.0125):** Does the Test interface change the conversion probability at each funnel transition?
   → **Mixed.** Significant improvement at `start → step_1`; significant *increase in drop-off* at `step_1 → step_2`; later transitions not significant.

Supplementary checks in the Bonus section: **Cohen's h** effect size and **post-hoc statistical power** for the completion-rate test, plus a **prospective power analysis** (minimum sample size) for future experiments.

## Key Findings

| KPI | Control | Test | Verdict |
|---|---|---|---|
| Completion Rate | 65.6% | 69.3% | Test higher, statistically significant (p ≈ 5.96 × 10⁻¹⁹) |
| Cost-effectiveness (+5% relative uplift) | — | +5.66% observed | Not statistically confirmed (p = 0.149) |
| Backward-Transition (Error) Rate | 8.93% | 11.71% | Test higher — more revisiting/friction |
| Confirm-step duration (mean, filtered) | 156.8s | 221.6s | Test users hesitate longer at the final step |
| Step 1 duration (mean, filtered) | 47.53s | 58.47s | Test slower at step 1 |
| Traffic split | 46.6% | 53.4% | Mild Sample Ratio Mismatch (outside ±5%) |

**Bottom line:** The redesigned interface drives a statistically significant improvement in completion rate, but introduces friction at `step_1` and especially at the `confirm` step, and does **not** clear Vanguard's 5% cost-effectiveness bar with statistical confidence. The recommendation in the notebook is: don't roll out as-is; fix confirm-step and step_1 friction, then re-test.

## A Note on the Probability / Statistical Testing Cells for KPI 1

The notebook treats **Completion Rate** as an empirical probability — `P(Completion) = completed users / eligible users` — and builds a full statistical testing pipeline around it:

- A **95% confidence interval** for the Test–Control difference in completion probability (`confint_proportions_2indep`)
- A **two-proportion z-test** for statistical significance (`proportions_ztest`)
- A **one-tailed z-test** against the +5% cost-effectiveness threshold
- **Cohen's h** effect size and **post-hoc power** for the completion-rate test
- A **prospective power analysis** (minimum required sample size for a future test)

**Why this was done for completion rate specifically:**
- It's the **primary business KPI** — the one metric the go/no-go rollout decision hinges on, per the stated business question and the +5% cost-effectiveness threshold.
- It's a **binary/proportion outcome** (completed vs not), which is exactly the case two-proportion z-tests, proportion confidence intervals, and Cohen's h are built for — the statistical toolkit fits cleanly.
- Framing it as a probability makes the result directly interpretable as a business statement ("X out of every 100 comparable users complete the process"), which supports the rollout decision more directly than a plain descriptive percentage would.

**Why it wasn't extended to the other KPIs (time spent, error rate, and the demographic/segment cuts):**
- Time-spent is a **continuous, right-skewed** variable — it would need a different test (e.g. Mann–Whitney U or a t-test on log-transformed data), not the proportion tests used for completion rate.
- Error rate (backward-transition rate) is also a proportion and *could* have been tested the same way, but wasn't — this is the more defensible omission to revisit.
- The demographic/segment cuts (by age, tenure, balance, logons) are exploratory breakdowns of the same completion-rate metric, not independent KPIs — testing every cut individually would also introduce a multiple-comparisons problem similar to what's already handled with the Bonferroni correction in Hypothesis 3.

**Relevance to the "take it out" decision:** Because the probability/inferential-statistics work is tightly scoped to completion rate — the one KPI the business decision (rollout vs no rollout) actually depends on — it's reasonable to leave it in even though it wasn't replicated for every KPI: not every KPI needs a formal significance test to be useful, and doing so for all ~10 would add substantial complexity without changing the recommendation. If your partners remove it purely for *consistency* reasons, consider keeping at minimum the two-proportion z-test and 95% CI for completion rate (Hypothesis 1) and the cost-effectiveness test (Hypothesis 2), since the report's core recommendation ("promising but not yet cost-effective") rests on those two results — descriptive completion-rate percentages alone don't support that conclusion. The Cohen's h/power-analysis cells (Bonus section) are the most self-contained to remove without affecting the rest of the notebook, since nothing downstream depends on them.

## Data Quality Notes & Known Issues

- **`client_last_step` vs furthest-step-reached:** early in the notebook, `client_last_step` is built from each client's most recent event overall, which can span multiple separate visits. The notebook explicitly moves away from this in favor of a **furthest-step-reached** metric (`step_rank` / `furthest_step_reached`) for completion, since a client's last chronological action isn't necessarily their most advanced one.
- **Duration outliers:** ~0.14% of step transitions exceed 30 minutes (up to 11+ hours), which likely reflects idle sessions rather than active use. These are excluded from the primary time-spent KPI, with the unfiltered data kept for reference.
- **Confirm-step duration:** excluded from the primary time-spent KPI (KPI 2) after a sensitivity check showed it disproportionately affects the Test group's average — it's reported separately as the Confirm Step Friction Score (KPI 7) instead.
- **Sample Ratio Mismatch:** the Test/Control traffic split (53.4% / 46.6%) falls slightly outside the ±5% tolerance typically expected for a clean 50/50 randomization. This doesn't invalidate the experiment but should be disclosed alongside the results.

## Outputs

- `tableau_export.csv` — event-level dataset (one row per interaction) with completion, time-per-step, and error-rate fields attached, for exploration in Tableau.
- `app.py` — a Streamlit dashboard skeleton (written via `%%writefile`, not executed inline) for a real-time Test vs Control KPI view. Requires `clients_df.to_csv("clients_df.csv")` to be run first, then `streamlit run app.py` from a terminal.
