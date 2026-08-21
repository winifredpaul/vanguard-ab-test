# Vanguard UI Redesign — Experiment Analysis

## Project Overview

This project evaluates a Vanguard A/B experiment comparing the existing digital experience (**Control**) with a redesigned digital experience (**Test**).

The experiment ran from **15 March 2017 to 20 June 2017**. The primary business question is:

> **Did the redesigned digital experience improve client completion enough to justify rollout?**

The analysis combines client-profile information, digital interaction data, and experiment assignment data to evaluate completion, funnel behaviour, time spent, backward navigation, client segments, statistical significance, and cost-effectiveness.

## Business Objectives

The project evaluates whether the redesign:

- Improves process completion.
- Changes step-level funnel behaviour.
- Introduces or reduces navigation friction.
- Changes time spent across process steps.
- Produces statistically significant improvements.
- Clears Vanguard's **5% relative completion-uplift threshold**.
- Supports a defensible rollout recommendation.

## Data Sources

The analysis uses four source datasets:

1. **Client demographics** — age, gender, tenure, number of accounts, balance, calls and logons.
2. **Web activity — part 1** — event-level digital interactions.
3. **Web activity — part 2** — additional event-level digital interactions.
4. **Experiment clients** — assignment to `Control` or `Test`.

The source datasets used for the analysis are included in the [`data/`](./data/) folder.

The two web-activity datasets are combined, duplicate events are checked/removed, and timestamps are converted to datetime values.

### Data Files

- [`df_final_demo.txt`](./data/df_final_demo.txt)
- [`df_final_experiment_clients.txt`](./data/df_final_experiment_clients.txt)
- [`df_final_web_data_pt_1.txt`](./data/df_final_web_data_pt_1.txt)
- [`df_final_web_data_pt_2.txt`](./data/df_final_web_data_pt_2.txt)

The processed event-level dataset used for the Tableau analysis is:

- [`tableau_export.csv`](./data/tableau_export.csv)

## Analysis Population

The notebook distinguishes between the broader experiment population and the profile-based analysis population:

- **Full experiment population:** 50,500 clients.
- **Profile-complete population used where required:** 50,487 clients.
- The profile-based population is smaller because some clients do not have all required profile fields.

The profile-complete population should not be presented as the total experiment size.

## Methodology

### Data Cleaning & Preparation

The workflow:

- Standardizes column names.
- Checks data types, missing values and duplicates.
- Validates experiment assignment values.
- Combines the two web-event datasets.
- Removes duplicate web events.
- Converts event timestamps to datetime.
- Orders process steps as `start → step_1 → step_2 → step_3 → confirm`.
- Identifies the furthest process step reached by each client.
- Builds client-level and event-level analysis datasets.

### Exploratory Data Analysis

The notebook examines age, gender, tenure, number of accounts, balance, calls, logons, and Test vs Control group composition.

### Performance KPIs

**KPI 1 — Completion Rate**
- Percentage of clients reaching `confirm`.

**KPI 2 — Time Spent per Step**
- Event-to-next-event duration within the same visit.
- Durations over 30 minutes are excluded as unrealistic inactive-session gaps.
- The primary step-time KPI focuses on `start`, `step_1`, `step_2`, and `step_3`.
- `confirm` duration is retained separately as a sensitivity/friction measure.

**KPI 3 — Backward Transition Rate**
- Measures navigation from a later process step back to an earlier one.

**KPI 4 — Funnel Drop-Off**
- Measures step-to-step retention/drop-off.

**Additional segment KPIs**
- Completion by age.
- Completion by digital engagement.
- Completion by tenure.
- Completion by balance tier.
- Traffic split.
- Confirm-step friction.

# Hypothesis Testing

## H1 — Completion Rate

### Question

Did the redesigned UI change completion rate?

### Hypotheses

- **H₀:** Test completion rate = Control completion rate.
- **H₁:** Test completion rate ≠ Control completion rate.

A two-proportion z-test is used.

### Result

- **Control completion:** 65.59%
- **Test completion:** 69.29%
- **Absolute uplift:** +3.71 percentage points
- **Relative uplift:** approximately +5.66%
- **Z-statistic:** approximately 8.89
- **P-value:** approximately 5.96 × 10⁻¹⁹

### Conclusion

**Reject H₀.** The redesigned experience produces a statistically significant improvement in completion.

## H2 — Cost-Effectiveness Threshold

Vanguard's business threshold is a **5% relative uplift**, not 5 percentage points.

### Hypotheses

- **H₀:** Test completion rate does not exceed Control by more than 5% relative uplift.
- **H₁:** Test completion rate exceeds Control by more than 5% relative uplift.

The 5% relative threshold is converted into the corresponding absolute difference before the one-sided proportion test.

### Result

- **Observed relative uplift:** +5.66%
- **Required relative uplift:** +5.00%
- **Observed result:** Above the business threshold
- **Z-statistic:** approximately 1.04
- **P-value:** approximately 0.149

### Conclusion

The observed point estimate exceeds Vanguard's 5% threshold, but the evidence is **not statistically sufficient to confirm that the true uplift exceeds 5%** at α = 0.05.

> **The point estimate clears the 5% threshold, but cost-effectiveness above that threshold is not statistically established.**

## H3 — Step-Level Funnel Conversion

The analysis tests:

1. Start → Step 1
2. Step 1 → Step 2
3. Step 2 → Step 3
4. Step 3 → Confirm

A two-proportion test is applied to each transition.

Because four simultaneous tests are performed, a Bonferroni correction is applied:

**α = 0.05 / 4 = 0.0125**

### Conclusion

- **Start → Step 1:** significantly improves progression.
- **Step 1 → Step 2:** significantly worsens progression.
- **Step 2 → Step 3:** not statistically significant.
- **Step 3 → Confirm:** not statistically significant.

The key product implication is that the redesign improves the beginning of the journey but introduces measurable friction between Step 1 and Step 2.

## Key Findings

### Completion

**Test: 69.3% vs Control: 65.6%**

The redesign materially and statistically significantly improves overall completion.

### Funnel

The effect is not uniform across the funnel. The strongest positive change occurs at **Start → Step 1**, while **Step 1 → Step 2** is the main statistically significant negative transition.

### Navigation Friction

The Test group has a higher overall backward-transition rate than Control, indicating more revisiting/backtracking behaviour.

### Time

After excluding inactive gaps over 30 minutes, the primary step-time analysis focuses on the active journey through Step 3. The notebook's sensitivity analysis retains confirm-step duration separately.

### Cost-Effectiveness

The observed +5.66% relative uplift is above Vanguard's +5% business threshold, but the H2 test does not statistically confirm that the true uplift exceeds the threshold.

## Experiment Evaluation & Limitations

The notebook evaluates experiment allocation, experiment duration, sample-ratio imbalance, availability of demographic data, interaction-level data limitations, and longer-term outcome limitations.

The experiment allocation is not perfectly balanced:

- **Control:** approximately 46.6%
- **Test:** approximately 53.4%

This mild imbalance should be acknowledged when interpreting results and considered in future experimental design.

Additional data that would strengthen a follow-up experiment includes:

- Device and browser information.
- Technical error and page-load data.
- Click-level interaction data.
- Detailed navigation paths.
- Qualitative client feedback.
- Longer-term outcomes.

## Recommendation

### **REFINE → INVESTIGATE → POWER & RETEST**

1. **Refine** — Address the statistically significant **Step 1 → Step 2** friction.
2. **Investigate** — Understand additional backward navigation and time/friction signals using deeper interaction-level data.
3. **Power & Retest** — Conduct a properly powered follow-up experiment and reassess whether the redesigned experience can reliably exceed Vanguard's +5% relative uplift threshold.

### Rollout Decision

**Do not roll out the redesign as-is.**

The redesign is promising because completion improves significantly, but the evidence does not statistically establish that the true uplift exceeds the business threshold.

## Tableau Presentation & Deliverable

The project findings are presented through the final Tableau Story. The Tableau Story serves as the presentation of the experiment analysis and includes:

1. Test Design & Objectives
2. Completion & Cost-Effectiveness
3. Funnel & Friction
4. Client Overview
5. Project Evaluation & Limitations
6. Results & Recommendations

The final packaged Tableau workbook is:

[`Vanguard_Tableau_Final.twbx`](./Vanguard_Tableau_Final.twbx)

The Tableau-ready event-level dataset used by the workbook is:

[`tableau_export.csv`](./data/tableau_export.csv)

## How to Run the Python Script

The accompanying script is:

```text
Vanguard_UI_Project_Final.py
```

Install the main dependencies:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

Then run:

```bash
python Vanguard_UI_Project_Final.py
```

The script loads the source datasets from the project's GitHub repository, performs the core analysis, and creates the Tableau-ready export.

Internet access is required unless the source URLs are replaced with local file paths.

## Final Submission Structure

```text
vanguard-ab-test/
├── README.md
├── Link to Kanban board.txt
├── Vanguard_Tableau_Final.twbx
├── Vanguard_UI_Project_Final.ipynb
├── Vanguard_UI_Project_Final.py
└── data/
    ├── df_final_demo.txt
    ├── df_final_experiment_clients.txt
    ├── df_final_web_data_pt_1.txt
    ├── df_final_web_data_pt_2.txt
    └── tableau_export.csv
## Project Management

The project Kanban board is maintained in Trello:

[View the Vanguard Project Kanban Board](https://trello.com/b/mwoWVmwQ/vangard-project)

## Note on the Notebook

The notebook contains exploratory material and later updated executive-ready sections. Some earlier exploratory markdown cells contain superseded hypothesis wording or conclusions from earlier iterations.

For the final submission, the intended analytical framing is the updated final sections:

- H1 — Completion Rate
- H2 — 5% Relative Cost-Effectiveness Threshold
- H3 — Step-Level Funnel Conversion with Bonferroni correction
- KPI 2 primary time analysis excluding `confirm`
- Event-level Tableau export

This README follows that final analytical framing rather than treating superseded exploratory text as the final conclusion.
