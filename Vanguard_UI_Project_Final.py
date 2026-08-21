# Vanguard UI Redesign — Experiment Analysis
# Generated from Vanguard_UI_Project_Final.ipynb
#
# This script contains the core reproducible analysis workflow:
# data loading, cleaning, experiment construction, KPI calculations,
# hypothesis testing, and Tableau export.
#
# It is intended to be run from a Python environment with internet access
# because the source datasets are loaded from the project GitHub repository.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
from statsmodels.stats.power import NormalIndPower


# --- Notebook cell 2 ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
import streamlit as st
from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.power import NormalIndPower


# --- Notebook cell 5 ---
df_final_demo = "https://raw.githubusercontent.com/winifredpaul/vanguard-ui-experiment-analysis/main/data/df_final_demo.txt"
df_final_web_data_pt_1 = "https://raw.githubusercontent.com/winifredpaul/vanguard-ui-experiment-analysis/main/data/df_final_web_data_pt_1.zip"
df_final_web_data_pt_2 = "https://raw.githubusercontent.com/winifredpaul/vanguard-ui-experiment-analysis/main/data/df_final_web_data_pt_2.zip"
df_final_experiment_clients = "https://raw.githubusercontent.com/winifredpaul/vanguard-ui-experiment-analysis/main/data/df_final_experiment_clients.txt"
clients_demo_df = pd.read_csv(df_final_demo)
web_data_pt1_df = pd.read_csv(df_final_web_data_pt_1, compression="zip")
web_data_pt2_df = pd.read_csv(df_final_web_data_pt_2, compression="zip")
experiment_clients_df = pd.read_csv(df_final_experiment_clients)


# --- Notebook cell 6 ---
# Quick check that all four data URLs are reachable before loading them
for name, url in [
    ("df_final_demo", df_final_demo),
    ("df_final_web_data_pt_1", df_final_web_data_pt_1),
    ("df_final_web_data_pt_2", df_final_web_data_pt_2),
    ("df_final_experiment_clients", df_final_experiment_clients),
]:
    status = requests.head(url, allow_redirects=True).status_code
    print(f"{name}: HTTP {status}")


# --- Notebook cell 11 ---
# Standardize column names for clarity
clients_demo_df = clients_demo_df.rename(
    columns={
        "clnt_tenure_yr": "client_tenure_year",
        "clnt_tenure_mnth": "client_tenure_months",
        "clnt_age": "client_age",
        "gendr": "gender",
        "num_accts": "number_of_accounts",
        "bal": "balance",
        "calls_6_mnth": "calls_last_6_months",
        "logons_6_mnth": "logons_last_6_months",
    }
)


# --- Notebook cell 12 ---
# Check data types and non-null counts for each column
clients_demo_df.info()


# --- Notebook cell 13 ---
# Count missing values in each column
clients_demo_df.isnull().sum()


# --- Notebook cell 14 ---
# Isolate rows that have any missing values, for closer inspection
clients_demo_df[clients_demo_df.isnull().any(axis=1)]


# --- Notebook cell 15 ---
# Check for fully duplicated rows (all columns identical)
clients_demo_df.duplicated().sum()


# --- Notebook cell 16 ---
# Check for duplicate client IDs specifically (different from full-row duplicates)
clients_demo_df["client_id"].duplicated().sum()


# --- Notebook cell 17 ---
# Check the distinct values in the gendr column
clients_demo_df["gender"].unique()


# --- Notebook cell 18 ---
# Check how many clients fall into each gender category
clients_demo_df["gender"].value_counts()


# --- Notebook cell 19 ---
# Review summary statistics (mean, min, max, quartiles) for the numeric columns
clients_demo_df.describe()


# --- Notebook cell 20 ---
# Look at the youngest clients to check the age data makes sense
clients_demo_df.sort_values("client_age").head()


# --- Notebook cell 22 ---
# Check if clnt_tenure_yr = floor(clnt_tenure_mnth / 12)
clients_demo_df["tenure_check_correct"] = (clients_demo_df["client_tenure_months"] // 12)

clients_demo_df[["client_tenure_year", "client_tenure_months", "tenure_check_correct"]].head(10)


# --- Notebook cell 24 ---
web_data_pt1_df.head()


# --- Notebook cell 25 ---
# Check data types and non-null counts for the first web activity file
web_data_pt1_df.info()


# --- Notebook cell 26 ---
# Check for missing values
web_data_pt1_df.isnull().sum()


# --- Notebook cell 27 ---
# Check for fully duplicated rows
web_data_pt1_df.duplicated().sum()


# --- Notebook cell 28 ---
# Preview the first few rows to understand the structure of the web activity log
web_data_pt1_df.head()


# --- Notebook cell 29 ---
# Check the distinct process steps to confirm the expected funnel stages
web_data_pt1_df["process_step"].unique()


# --- Notebook cell 30 ---
# Check how many unique visitors and sessions are captured in this file
print("Unique visitors:", web_data_pt1_df["visitor_id"].nunique())
print("Unique visits:", web_data_pt1_df["visit_id"].nunique())


# --- Notebook cell 31 ---
# Check the date range covered by this file
web_data_pt1_df["date_time"] = pd.to_datetime(web_data_pt1_df["date_time"])
print("First activity:", web_data_pt1_df["date_time"].min())
print("Last activity:", web_data_pt1_df["date_time"].max())


# --- Notebook cell 33 ---
# overview of the dataset
web_data_pt2_df.head()


# --- Notebook cell 34 ---
# Check data types and non-null counts for the second web activity file
web_data_pt2_df.info()


# --- Notebook cell 35 ---
# Check for missing values
web_data_pt2_df.isnull().sum()


# --- Notebook cell 36 ---
# Check for fully duplicated rows
web_data_pt2_df.duplicated().sum()


# --- Notebook cell 37 ---
# Preview the first few rows to confirm this file matches pt_1's structure
web_data_pt2_df.head()


# --- Notebook cell 38 ---
# Check the distinct process steps match pt_1's funnel stages
web_data_pt2_df["process_step"].unique()


# --- Notebook cell 39 ---
# Check how many unique visitors and sessions are captured in this file
print("Unique visitors:", web_data_pt2_df["visitor_id"].nunique())
print("Unique visits:", web_data_pt2_df["visit_id"].nunique())


# --- Notebook cell 40 ---
# Check the date range covered by this file
web_data_pt2_df["date_time"] = pd.to_datetime(web_data_pt2_df["date_time"])
print("First activity:", web_data_pt2_df["date_time"].min())
print("Last activity:", web_data_pt2_df["date_time"].max())


# --- Notebook cell 41 ---
# Confirm both web data files have identical columns, in the same order,
# before combining them with pd.concat()
list(web_data_pt1_df.columns) == list(web_data_pt2_df.columns)


# --- Notebook cell 43 ---
# Check data types and non-null counts for the experiment roster
experiment_clients_df.info()


# --- Notebook cell 44 ---
# Check for missing Variation values (clients not part of the experiment)
experiment_clients_df.isnull().sum()


# --- Notebook cell 45 ---
# Check for fully duplicated rows
experiment_clients_df.duplicated().sum()


# --- Notebook cell 46 ---
# Check for duplicate client IDs in the roster
experiment_clients_df["client_id"].duplicated().sum()


# --- Notebook cell 47 ---
# Standardize column names
experiment_clients_df = experiment_clients_df.rename(
    columns={"Variation": "variation"}
)
# verify the changes
print(experiment_clients_df.columns)


# --- Notebook cell 48 ---
# Confirm the only possible values are Test, Control, or missing
experiment_clients_df["variation"].unique()


# --- Notebook cell 49 ---
# Check how many clients are in each experiment group
experiment_clients_df["variation"].value_counts(dropna=False)


# --- Notebook cell 51 ---
# STEP 1: Count unique clients in dataset 1
dataset_1_clients = clients_demo_df["client_id"].nunique()

# STEP 2: Count unique clients assigned to the experiment (exclude NaN)
dataset_4_clients = (
    experiment_clients_df
    .loc[experiment_clients_df["variation"].notna(), "client_id"]
    .nunique()
)

# STEP 3: Find clients appearing in both datasets
overlapping_clients = clients_demo_df.merge(
    experiment_clients_df,
    on="client_id",
    how="inner"
)

# STEP 4: Count unique overlapping clients who participated in the experiment
overlap_count = (
    overlapping_clients
    .loc[overlapping_clients["variation"].notna(), "client_id"]
    .nunique()
)

# STEP 5: Display the results
print("Unique clients in dataset 1:", dataset_1_clients)
print("Unique experiment clients:", dataset_4_clients)
print("Clients appearing in both datasets:", overlap_count)

# STEP 6: Preview the overlapping clients
overlapping_clients.head(10)


# --- Notebook cell 53 ---
# Merge the Variation column from the experiment roster into the demo dataset
# Using a left join keeps every client, whether or not they were part of the experiment
clients_demo_exp_df = clients_demo_df.merge(
    experiment_clients_df[["client_id", "variation"]],
    on="client_id",
    how="left"
)

# Flag whether each client was part of the experiment
clients_demo_exp_df["part_of_experiment"] = clients_demo_exp_df["variation"].notna().map({
    True: "Yes",
    False: "No"
})

clients_demo_exp_df.head()


# --- Notebook cell 54 ---
# Confirm structure and non-null counts after the merge
clients_demo_exp_df.info()


# --- Notebook cell 55 ---
# Check how many clients fall into each group, including those not in the experiment
clients_demo_exp_df["variation"].value_counts(dropna=False)


# --- Notebook cell 56 ---
# Check gender distribution across Test/Control/not-in-experiment groups
gender_by_variation = pd.crosstab(
    clients_demo_exp_df["variation"],
    clients_demo_exp_df["gender"]
)
print(gender_by_variation)


# --- Notebook cell 59 ---
# Stack the two web activity files into one (they share identical columns)
combined_web_data_df = pd.concat(
    [web_data_pt1_df, web_data_pt2_df],
    ignore_index=True
)

combined_web_data_df.info()


# --- Notebook cell 60 ---
# Check for duplicate rows introduced by combining the two files
combined_web_data_df.duplicated().sum()


# --- Notebook cell 61 ---
# Remove duplicate rows so events aren't double-counted downstream
combined_web_data_df = combined_web_data_df.drop_duplicates()

# Confirm no duplicates remain
combined_web_data_df.duplicated().sum()


# --- Notebook cell 62 ---
# Confirm the combined file still only has the expected funnel stages
combined_web_data_df["process_step"].unique()


# --- Notebook cell 63 ---
# Convert date_time to a proper datetime type
combined_web_data_df["date_time"] = pd.to_datetime(combined_web_data_df["date_time"])


# --- Notebook cell 65 ---
# Check the overall date range and confirm all activity falls within the experiment window
print("First activity:", combined_web_data_df["date_time"].min())
print("Last activity:", combined_web_data_df["date_time"].max())

experiment_start = pd.Timestamp("2017-03-15")
experiment_end = pd.Timestamp("2017-06-21")

outside_experiment = combined_web_data_df[
    (combined_web_data_df["date_time"] < experiment_start) | (combined_web_data_df["date_time"] > experiment_end)
]

print(f"\nActivities outside the experiment period: {len(outside_experiment)}")
outside_experiment.tail()


# --- Notebook cell 66 ---
# Spot-check one client's full activity history, sorted chronologically
client_id = 934

(
    combined_web_data_df[combined_web_data_df["client_id"] == client_id]
    .sort_values("date_time")
)


# --- Notebook cell 67 ---
# Spot-check a client who completed the process (reached "confirm")
# Useful to confirm their last row really does show process_step = "confirm"
client_id = combined_web_data_df.loc[
    combined_web_data_df["process_step"] == "confirm", "client_id"
].iloc[0]

(
    combined_web_data_df[combined_web_data_df["client_id"] == client_id]
    .sort_values("date_time")
)


# --- Notebook cell 68 ---
# Spot-check a client with multiple visits (visit_id changes),
# to see how groupby("client_id").last() behaves when someone has more than one session
multi_visit_clients = (
    combined_web_data_df.groupby("client_id")["visit_id"].nunique()
)
client_id = multi_visit_clients[multi_visit_clients > 1].index[0]

(
    combined_web_data_df[combined_web_data_df["client_id"] == client_id]
    .sort_values("date_time")
)


# --- Notebook cell 70 ---
# Define the order of the process, so we can measure "furthest step reached"
step_order = {
    "start": 0,
    "step_1": 1,
    "step_2": 2,
    "step_3": 3,
    "confirm": 4
}

# Map each process_step to its numeric rank
combined_web_data_df["step_rank"] = combined_web_data_df["process_step"].map(step_order)

# For each client, find the highest step rank they ever reached
furthest_step = (
    combined_web_data_df
    .groupby("client_id")["step_rank"]
    .max()
    .reset_index()
)

# Map the numeric rank back to a readable step name
rank_to_step = {v: k for k, v in step_order.items()}
furthest_step["furthest_step_reached"] = furthest_step["step_rank"].map(rank_to_step)

furthest_step.head()


# --- Notebook cell 71 ---
# Merge the furthest step reached into the demographics + experiment dataframe
clients_demo_exp_df = clients_demo_exp_df.merge(
    furthest_step[["client_id", "furthest_step_reached"]],
    on="client_id",
    how="left"
)

clients_demo_exp_df.head()


# --- Notebook cell 72 ---
# Keep only clients who were actually assigned to Test or Control
experiment_only_df = clients_demo_exp_df[
    clients_demo_exp_df["variation"].isin(["Test", "Control"])
].copy()

# Drop the participation flag — every row here is an experiment client by definition
experiment_only_df = experiment_only_df.drop(columns=["part_of_experiment"])

experiment_only_df.info()


# --- Notebook cell 74 ---
# Confirm the Test/Control split
experiment_only_df["variation"].value_counts(dropna=False)


# --- Notebook cell 75 ---
# Inspect rows with missing demographic data before dropping them
missing_rows = experiment_only_df[experiment_only_df.isnull().any(axis=1)]
missing_rows


# --- Notebook cell 76 ---
# Drop rows with missing values — this is the analysis-ready experiment dataset
experiment_final_df = experiment_only_df.dropna()

experiment_final_df.info()


# --- Notebook cell 78 ---
# Sort chronologically so each client's most recent event is last
combined_web_data_df = combined_web_data_df.sort_values("date_time")

# Get each client's latest recorded event
client_last_step = (
    combined_web_data_df
    .groupby("client_id")
    .last()
    .reset_index()
)

# Add each client's experiment group assignment
client_last_step = client_last_step.merge(
    experiment_clients_df[["client_id", "variation"]],
    on="client_id",
    how="left"
)

client_last_step[["client_id", "process_step", "variation"]].head(20)


# --- Notebook cell 79 ---
web_events_df = combined_web_data_df.merge(
    experiment_clients_df[["client_id", "variation"]],
    on="client_id",
    how="inner"
)

web_events_df = web_events_df[
    web_events_df["variation"].isin(["Test", "Control"])
].reset_index(drop=True)

print(web_events_df.info())


# --- Notebook cell 80 ---
group_sizes = (
    web_events_df.drop_duplicates(subset=["client_id"])["variation"]
    .value_counts()
)
group_sizes


# --- Notebook cell 81 ---
# 1. Event_Level dataset
clients_df = experiment_final_df.copy()

clients_df.info()


# --- Notebook cell 82 ---
clients_df.count()


# --- Notebook cell 104 ---
clients_df.columns


# --- Notebook cell 106 ---
# 7. Variation Distribution

clients_df["variation"].value_counts()


# --- Notebook cell 107 ---
# To check the percentage breakdown (proportions) of each group

clients_df["variation"].value_counts(normalize=True) * 100


# --- Notebook cell 113 ---
clients_df.groupby('variation').agg({
    'client_age': ['mean', 'std'],
    'client_tenure_year': ['mean', 'std'],
    'number_of_accounts': ['mean', 'std'],
    'balance': ['mean', 'std'],
    'logons_last_6_months': ['mean', 'std'],
    'calls_last_6_months': ['mean', 'std']
})


# --- Notebook cell 117 ---
# KPI 1: Completion Rate
# Process: start - step_1 - step_2 - step_3 - confirm

completion_rate_df = (
    clients_df.groupby("variation")
    ["furthest_step_reached"]
    .apply(lambda x:
           (x=="confirm").sum()/x.count())
)

completion_rate_df


# --- Notebook cell 118 ---
completion_df = (
     clients_df.assign(
        completed=lambda d: d["furthest_step_reached"].eq("confirm")
    )
    .groupby("variation")["completed"]
    .mean()
    .reset_index(name="completion_rate")
)
completion_df


# --- Notebook cell 120 ---
# Completion counts and totals per group (needed for the 95% CI below,
# and reused in Phase 3 hypothesis testing)
test_success = clients_df[(clients_df["variation"]=="Test") &
                           (clients_df["furthest_step_reached"]=="confirm")]["client_id"].nunique()

ctrl_success = clients_df[(clients_df["variation"]=="Control") &
                           (clients_df["furthest_step_reached"]=="confirm")]["client_id"].nunique()

test_total = clients_df[clients_df["variation"]=="Test"]["client_id"].nunique()
ctrl_total = clients_df[clients_df["variation"]=="Control"]["client_id"].nunique()

test_rate = test_success / test_total
ctrl_rate = ctrl_success / ctrl_total

print("Test successes:", test_success, "| Test total:", test_total, "| Test rate:", f"{test_rate:.4%}")
print("Control successes:", ctrl_success, "| Control total:", ctrl_total, "| Control rate:", f"{ctrl_rate:.4%}")


# --- Notebook cell 122 ---
from statsmodels.stats.proportion import confint_proportions_2indep

# Completion rates
test_rate = test_success / test_total
ctrl_rate = ctrl_success / ctrl_total

# Difference in completion probabilities
completion_difference = test_rate - ctrl_rate

# 95% Confidence Interval for the difference
ci_low, ci_high = confint_proportions_2indep(
    count1=test_success,
    nobs1=test_total,
    count2=ctrl_success,
    nobs2=ctrl_total,
    method="wald"
)

print(f"Test completion rate: {test_rate:.4%}")
print(f"Control completion rate: {ctrl_rate:.4%}")
print(f"Difference in completion rates: {completion_difference:.4%}")
print(f"95% Confidence Interval: ({ci_low:.4%}, {ci_high:.4%})")


# --- Notebook cell 126 ---
# Define the expected order of the funnel

step_order = {
    "start": 0,
    "step_1": 1,
    "step_2": 2,
    "step_3": 3,
    "confirm": 4
}

funnel_client_df = experiment_final_df[
    ["client_id", "variation", "furthest_step_reached"]
].copy()

funnel_client_df["furthest_step_number"] = (
    funnel_client_df["furthest_step_reached"].map(step_order)
)

funnel_client_df.head()


# --- Notebook cell 128 ---
# Calculate the number and percentage of clients reaching each funnel stage

funnel_rows = []

for variation in ["Control", "Test"]:
    group = funnel_client_df[
        funnel_client_df["variation"] == variation
    ]

    total_clients = group["client_id"].nunique()

    for step_name, step_number in step_order.items():
        clients_reached = (
            group["furthest_step_number"] >= step_number
        ).sum()

        funnel_rows.append({
            "variation": variation,
            "process_step": step_name,
            "clients_reached": clients_reached,
            "reach_rate": clients_reached / total_clients
        })

funnel_summary = pd.DataFrame(funnel_rows)

funnel_summary


# --- Notebook cell 130 ---
# Calculate step-to-step conversion and drop-off

funnel_summary["previous_clients_reached"] = (
    funnel_summary
    .groupby("variation")["clients_reached"]
    .shift(1)
)

funnel_summary["step_conversion_rate"] = (
    funnel_summary["clients_reached"]
    / funnel_summary["previous_clients_reached"]
)

funnel_summary["drop_off_rate"] = (
    1 - funnel_summary["step_conversion_rate"]
)

funnel_summary


# --- Notebook cell 132 ---
# Compare conversion and drop-off rates side by side

funnel_comparison = funnel_summary.pivot(
    index="process_step",
    columns="variation",
    values=["step_conversion_rate", "drop_off_rate"]
)

funnel_comparison


# --- Notebook cell 134 ---
# Create a clean comparison table

funnel_difference = pd.DataFrame({
    "Control Conversion": funnel_comparison["step_conversion_rate"]["Control"],
    "Test Conversion": funnel_comparison["step_conversion_rate"]["Test"],
    "Conversion Difference": (
        funnel_comparison["step_conversion_rate"]["Test"]
        - funnel_comparison["step_conversion_rate"]["Control"]
    ),
    "Control Drop-off": funnel_comparison["drop_off_rate"]["Control"],
    "Test Drop-off": funnel_comparison["drop_off_rate"]["Test"],
    "Drop-off Difference": (
        funnel_comparison["drop_off_rate"]["Test"]
        - funnel_comparison["drop_off_rate"]["Control"]
    )
})

funnel_difference


# --- Notebook cell 135 ---
# Add clear transition labels for interpretation

transition_labels = {
    "step_1": "start → step_1",
    "step_2": "step_1 → step_2",
    "step_3": "step_2 → step_3",
    "confirm": "step_3 → confirm"
}

funnel_difference = funnel_difference.drop(index="start").copy()

funnel_difference["transition"] = (
    funnel_difference.index.map(transition_labels)
)

funnel_difference


# --- Notebook cell 139 ---
# Combine both web activity datasets (already done earlier as combined_web_data_df,
# reused here) and merge with the experiment roster so every event is labelled
# Test or Control.
web_events_df = combined_web_data_df.merge(
    experiment_clients_df[["client_id", "variation"]],
    on="client_id",
    how="inner"
)

# Keep only Test and Control
web_events_df = web_events_df[
    web_events_df["variation"].isin(["Test", "Control"])
].copy()

# Sort events chronologically within each visit — required before calculating
# time between consecutive steps
web_events_df = web_events_df.sort_values(
    ["visit_id", "date_time"]
).reset_index(drop=True)


# --- Notebook cell 140 ---
# Validate the event-level dataset

print("Rows:", len(web_events_df))
print("Unique clients:", web_events_df["client_id"].nunique())
print("Unique visits:", web_events_df["visit_id"].nunique())

print("\nVariation counts:")
print(web_events_df["variation"].value_counts())

web_events_df.head()


# --- Notebook cell 141 ---
# Build the event-level dataset for KPI 2 (time spent per step) from
# web_events_df. `df` is local to this KPI-2 block; KPI 3 (Error Rate)
# builds its own copy of web_events_df later and is independent of this one.
df = web_events_df.copy()
df = df.sort_values(["visitor_id", "visit_id", "date_time"])

df["next_step"] = df.groupby(["visitor_id", "visit_id"])["process_step"].shift(-1)

# Next timestamp within the same visit -> time spent on the current step
df["next_date_time"] = df.groupby(["visitor_id", "visit_id"])["date_time"].shift(-1)
df["duration"] = (df["next_date_time"] - df["date_time"]).dt.total_seconds()

# Drop the final event of each visit (no next step = no duration) and
# remove negative durations if they exist
time_df = df.dropna(subset=["duration"]).copy()
time_df = time_df[time_df["duration"] >= 0]

time_df.head()


# --- Notebook cell 143 ---
# Inspect event gaps longer than 30 minutes

duration_outliers_df = time_df[
    time_df["duration"] > 1800
].copy()

print("Total valid transitions:", len(time_df))
print("Transitions > 30 minutes:", len(duration_outliers_df))

print(
    f"Percentage > 30 minutes: "
    f"{len(duration_outliers_df) / len(time_df) * 100:.2f}%"
)

duration_outliers_df[
    [
        "client_id",
        "visit_id",
        "variation",
        "process_step",
        "next_step",
        "duration"
    ]
].sort_values(
    "duration",
    ascending=False
).head(20)


# --- Notebook cell 145 ---
# Remove unrealistic inactive sessions (>30 minutes)

duration_filtered_df = time_df[
    time_df["duration"] <= 1800
].copy()

print("Transitions before filtering:", len(time_df))
print("Transitions after filtering:", len(duration_filtered_df))

duration_filtered_df["duration"].describe()


# --- Notebook cell 147 ---
# Summarize duration by experiment group and process step

duration_summary_filtered = (
    duration_filtered_df
    .groupby(["variation", "process_step"])
    .agg(
        transition_count=("duration", "count"),
        average_seconds=("duration", "mean"),
        median_seconds=("duration", "median")
    )
    .reset_index()
)

duration_summary_filtered["average_minutes"] = (
    duration_summary_filtered["average_seconds"] / 60
)

duration_summary_filtered["median_minutes"] = (
    duration_summary_filtered["median_seconds"] / 60
)

duration_summary_filtered


# --- Notebook cell 149 ---
# Compare overall duration results with and without the confirm step

with_confirm = (
    duration_filtered_df
    .groupby("variation")["duration"]
    .agg(
        average_with_confirm="mean",
        median_with_confirm="median"
    )
)

without_confirm = (
    duration_filtered_df[
        duration_filtered_df["process_step"] != "confirm"
    ]
    .groupby("variation")["duration"]
    .agg(
        average_without_confirm="mean",
        median_without_confirm="median"
    )
)

confirm_impact = with_confirm.join(without_confirm)

confirm_impact["average_difference"] = (
    confirm_impact["average_without_confirm"]
    - confirm_impact["average_with_confirm"]
)

confirm_impact["median_difference"] = (
    confirm_impact["median_without_confirm"]
    - confirm_impact["median_with_confirm"]
)

confirm_impact.round(2)


# --- Notebook cell 152 ---
# Create the final KPI 2 summary excluding confirm

duration_kpi_df = duration_summary_filtered[
    duration_summary_filtered["process_step"] != "confirm"
].copy()

duration_kpi_df


# --- Notebook cell 153 ---
# Compare average and median duration by process step

duration_comparison = duration_kpi_df.pivot(
    index="process_step",
    columns="variation",
    values=["average_seconds", "median_seconds"]
)

duration_comparison


# --- Notebook cell 158 ---
# KPI 3: Backward Transition Rate by Step

df = web_events_df.copy()
df = df.sort_values(["visitor_id", "visit_id", "date_time"])

# Identify the next step within each visit
df["next_step"] = (
    df.groupby(["visitor_id", "visit_id"])["process_step"]
      .shift(-1)
)

# Convert steps to numbers so we can identify backward movement
step_map = {
    "start": 0,
    "step_1": 1,
    "step_2": 2,
    "step_3": 3,
    "confirm": 4
}

df["step_num"] = df["process_step"].map(step_map)
df["next_step_num"] = df["next_step"].map(step_map)

# Keep only actual transitions
transitions = df.dropna(subset=["next_step_num"]).copy()

# Identify backward transitions
transitions["is_backward"] = (
    transitions["next_step_num"] < transitions["step_num"]
)

# Calculate backward-transition rate for EACH STEP and variation
backward_by_step = (
    transitions
    .groupby(["variation", "process_step"])["is_backward"]
    .agg(
        total_transitions="count",
        backward_transitions="sum"
    )
    .reset_index()
)

# Calculate rate
backward_by_step["backward_transition_rate"] = (
    backward_by_step["backward_transitions"]
    / backward_by_step["total_transitions"]
)

# Percentage
backward_by_step["backward_transition_rate_percent"] = (
    backward_by_step["backward_transition_rate"] * 100
)

backward_by_step


# --- Notebook cell 163 ---
# KPI 4. Step‑Level Drop‑Off Rate
funnel = (
    clients_df
    .groupby(["variation", "furthest_step_reached"])["client_id"]
    .nunique()
    .reset_index()
)

order = ["start", "step_1", "step_2", "step_3", "confirm"]
funnel["furthest_step_reached"] = pd.Categorical(funnel["furthest_step_reached"],
                                                 categories=order, ordered=True)
funnel


# --- Notebook cell 168 ---
# KPI 5: Completion Rate by Age Group

# Make a safe copy to avoid SettingWithCopyWarning
df = clients_df.copy()

# Create completed column
df["completed"] = df["furthest_step_reached"].eq("confirm")

# Create age groups safely
df["age_group"] = pd.cut(
    df["client_age"],
    bins=[18, 30, 45, 60, 100],
    labels=["18–30", "31–45", "46–60", "60+"],
    include_lowest=True
)

# Compute completion rate by age group
age_completion = (
    df.groupby(["age_group", "variation"], observed=True)["completed"]
    .mean()
    .reset_index(name="completion_rate")
)

age_completion


# --- Notebook cell 173 ---
# KPI 6: Completion Rate by Digital Engagement (Logons)
# Make a safe copy to avoid SettingWithCopyWarning
df = clients_df.copy()

# Create 'completed' column if not already present
df["completed"] = df["furthest_step_reached"].eq("confirm")

# Create engagement groups based on logons in the last 6 months
df["logon_group"] = pd.cut(
    df["logons_last_6_months"],
    bins=[0, 5, 15, 50, 200],
    labels=["Low", "Medium", "High", "Very High"],
    include_lowest=True
)

# Compute completion rate by engagement level and variation
logon_completion = (
    df.groupby(["logon_group", "variation"], observed=True)["completed"]
    .mean()
    .reset_index(name="completion_rate")
)

logon_completion


# --- Notebook cell 178 ---
# KPI 7: Confirm Step Friction Score (filtered — excludes idle sessions >30 min)

confirm_filtered = duration_filtered_df[
    duration_filtered_df["process_step"] == "confirm"
]

friction = (
    confirm_filtered
    .groupby("variation")["duration"]
    .agg(
        avg_confirm_duration="mean",
        median_confirm_duration="median",
        transition_count="count"
    )
    .reset_index()
)

friction


# --- Notebook cell 183 ---
# KPI 8: Traffic Split

traffic_split = (
    clients_df
    .groupby("variation")["client_id"]
    .nunique()
    .reset_index(name="n_users")
)

traffic_split["traffic_share_%"] = (
    traffic_split["n_users"] / traffic_split["n_users"].sum() * 100
)

traffic_split


# --- Notebook cell 189 ---
# KPI 9: Completion Rate by Tenure
df = clients_df.copy()

# Create completed column
df["completed"] = df["furthest_step_reached"].eq("confirm")

# Create tenure groups
df["tenure_group"] = pd.cut(
    df["client_tenure_year"],
    bins=[0, 2, 5, 10, 50],
    labels=["0–2 yrs", "3–5 yrs", "6–10 yrs", "10+ yrs"],
    include_lowest=True
)

# Compute completion rate by tenure and variation
tenure_completion = (
    df.groupby(["tenure_group", "variation"], observed=True)["completed"]
    .mean()
    .reset_index(name="completion_rate")
)

tenure_completion


# --- Notebook cell 194 ---
# KPI 10: Completion Rate by Balance Tier
df = clients_df.copy()

# Create completed column
df["completed"] = df["furthest_step_reached"].eq("confirm")

# Define balance tiers
df["balance_tier"] = pd.cut(
    df["balance"],
    bins=[0, 50000, 250000, 1000000, float("inf")],
    labels=["Low (<50K)", "Medium (50K–250K)", "High (250K–1M)", "Very High (>1M)"],
    include_lowest=True
)

# Compute completion rate by balance tier and variation
balance_completion = (
    df.groupby(["balance_tier", "variation"], observed=True)["completed"]
    .mean()
    .reset_index(name="completion_rate")
)

balance_completion


# --- Notebook cell 202 ---
# first build a completion rate DataFrame
completion = (
    experiment_final_df.groupby("variation")["furthest_step_reached"]
    .apply(lambda x: (x=="confirm").mean())
    .reset_index(name="completion_rate")
)


# --- Notebook cell 203 ---
# HYPOTHESIS 1: Two‑proportion z‑test(Completion Rate):

from statsmodels.stats.proportion import proportions_ztest
import numpy as np

test_success = clients_df[(clients_df["variation"]=="Test") &
                                   (clients_df["furthest_step_reached"]=="confirm")]["client_id"].nunique()

ctrl_success = clients_df[(clients_df["variation"]=="Control") &
                                   (clients_df["furthest_step_reached"]=="confirm")]["client_id"].nunique()

test_total = clients_df[clients_df["variation"]=="Test"]["client_id"].nunique()
ctrl_total = clients_df[clients_df["variation"]=="Control"]["client_id"].nunique()

count = np.array([test_success, ctrl_success])
nobs = np.array([test_total, ctrl_total])

z_stat, p_val = proportions_ztest(count, nobs, alternative="two-sided")
print(f"Z-statistic = {z_stat:.4f}")
print(f"P-value = {p_val:.4e}")


# --- Notebook cell 208 ---
# Calculate Vanguard's 5% relative uplift threshold

test_total = clients_df.loc[
    clients_df["variation"] == "Test",
    "client_id"
].nunique()

control_total = clients_df.loc[
    clients_df["variation"] == "Control",
    "client_id"
].nunique()

test_completed = clients_df.loc[
    (clients_df["variation"] == "Test") &
    (clients_df["furthest_step_reached"] == "confirm"),
    "client_id"
].nunique()

control_completed = clients_df.loc[
    (clients_df["variation"] == "Control") &
    (clients_df["furthest_step_reached"] == "confirm"),
    "client_id"
].nunique()

test_rate = test_completed / test_total
control_rate = control_completed / control_total

required_test_rate = control_rate * 1.05

observed_relative_improvement = (
    test_rate - control_rate
) / control_rate

print(f"Control completion rate: {control_rate:.2%}")
print(f"Test completion rate: {test_rate:.2%}")
print(f"Required Test rate for +5% uplift: {required_test_rate:.2%}")
print(f"Observed relative improvement: {observed_relative_improvement:.2%}")


# --- Notebook cell 209 ---
from statsmodels.stats.proportion import proportions_ztest
import numpy as np

counts = np.array([
    test_completed,
    control_completed
])

nobs = np.array([
    test_total,
    control_total
])

# 5% relative uplift expressed as required absolute difference
required_difference = control_rate * 0.05

z_stat_h2, p_value_h2 = proportions_ztest(
    counts,
    nobs,
    value=required_difference,
    alternative="larger"
)

print(f"Required absolute difference: {required_difference:.2%}")
print(f"Observed absolute difference: {(test_rate - control_rate):.2%}")
print(f"Z-statistic: {z_stat_h2:.4f}")
print(f"P-value: {p_value_h2:.6f}")


# --- Notebook cell 212 ---
# Prepare step-level conversion rates for hypothesis testing

step_order = ["start", "step_1", "step_2", "step_3", "confirm"]

transition_rows = []

for variation in ["Control", "Test"]:
    
    group = (
        funnel_summary[
            funnel_summary["variation"] == variation
        ]
        .set_index("process_step")
    )

    for i in range(len(step_order) - 1):
        
        from_step = step_order[i]
        to_step = step_order[i + 1]

        clients_from = int(group.loc[from_step, "clients_reached"])
        clients_to = int(group.loc[to_step, "clients_reached"])

        transition_rows.append({
            "Variation": variation,
            "transition": f"{from_step} → {to_step}",
            "clients_from": clients_from,
            "clients_to": clients_to,
            "conversion_rate": clients_to / clients_from,
            "drop_off_rate": 1 - (clients_to / clients_from)
        })

transition_df = pd.DataFrame(transition_rows)

transition_df


# --- Notebook cell 213 ---
from statsmodels.stats.proportion import proportions_ztest

hypothesis_3_results = []

transitions = transition_df["transition"].unique()

for transition in transitions:

    control = transition_df[
        (transition_df["Variation"] == "Control") &
        (transition_df["transition"] == transition)
    ].iloc[0]

    test = transition_df[
        (transition_df["Variation"] == "Test") &
        (transition_df["transition"] == transition)
    ].iloc[0]

    counts = np.array([
        test["clients_to"],
        control["clients_to"]
    ])

    nobs = np.array([
        test["clients_from"],
        control["clients_from"]
    ])

    z_stat, p_value = proportions_ztest(
        counts,
        nobs,
        alternative="two-sided"
    )

    hypothesis_3_results.append({
        "transition": transition,
        "control_conversion": control["conversion_rate"],
        "test_conversion": test["conversion_rate"],
        "difference": test["conversion_rate"] - control["conversion_rate"],
        "z_statistic": z_stat,
        "p_value": p_value
    })

hypothesis_3_results = pd.DataFrame(hypothesis_3_results)

hypothesis_3_results


# --- Notebook cell 214 ---
# Apply Bonferroni correction for four simultaneous tests

alpha = 0.05
n_tests = len(hypothesis_3_results)
bonferroni_alpha = alpha / n_tests

hypothesis_3_results["bonferroni_alpha"] = bonferroni_alpha

hypothesis_3_results["significant_after_bonferroni"] = (
    hypothesis_3_results["p_value"] < bonferroni_alpha
)

print(f"Original alpha: {alpha}")
print(f"Number of tests: {n_tests}")
print(f"Bonferroni-adjusted alpha: {bonferroni_alpha}")

hypothesis_3_results


# --- Notebook cell 223 ---
#a) Compare navigation paths (sequence of steps)
# Sequence of steps per visit — use the event-level web_events_df (one row
# per interaction), not clients_df (one row per client, no visit/step detail)
paths = (
    web_events_df
    .sort_values(["visitor_id", "visit_id", "date_time"])
    .groupby(["variation", "visitor_id", "visit_id"])["process_step"]
    .apply(lambda x: " \u2192 ".join(x))
    .reset_index(name="path")
)

# Top 10 most common paths per variation
paths_summary = (
    paths.groupby(["variation", "path"])["visitor_id"]
    .count()
    .reset_index(name="count")
    .sort_values(["variation", "count"], ascending=[True, False])
)

paths_summary.head(10)


# --- Notebook cell 225 ---
# b) Hypothesis: difference in number of actions (steps) between Test and Control
steps_per_visit = (
    web_events_df
    .groupby(["variation", "visitor_id", "visit_id"])["process_step"]
    .count()
    .reset_index(name="num_steps")
)

test_steps = steps_per_visit.loc[steps_per_visit["variation"]=="Test", "num_steps"]
ctrl_steps = steps_per_visit.loc[steps_per_visit["variation"]=="Control", "num_steps"]

t_stat, p_val_steps = ttest_ind(test_steps, ctrl_steps, equal_var=False)
t_stat, p_val_steps


# --- Notebook cell 227 ---
# a) Effect size (Cohen’s h for proportions)

p1 = test_success / test_total
p2 = ctrl_success / ctrl_total

def cohens_h(p1, p2):
    return 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))

h = cohens_h(p1, p2)
h


# --- Notebook cell 228 ---
# b) Post‑hoc power (using statsmodels)

effect_size = h
alpha = 0.05
power_analysis = NormalIndPower()

power = power_analysis.power(
    effect_size=effect_size,
    nobs1=test_total,
    alpha=alpha,
    ratio=ctrl_total/test_total,
    alternative='two-sided'
)
power


# --- Notebook cell 230 ---
# Assume expected proportions (from your current experiment or business expectation)
p1_expected = 0.70   # Test
p2_expected = 0.65   # Control

h_expected = cohens_h(p1_expected, p2_expected)

alpha = 0.05
target_power = 0.8
ratio = 1.0  # equal group sizes

power_analysis = NormalIndPower()
n_required = power_analysis.solve_power(
    effect_size=h_expected,
    alpha=alpha,
    power=target_power,
    ratio=ratio,
    alternative='two-sided'
)
n_required


# --- Notebook cell 233 ---
# ============================================
# TABLEAU EXPORT - ONE EVENT-LEVEL DATASET
# ============================================

import pandas as pd
import numpy as np

# Start from the experiment event-level data
tableau_df = web_events_df.copy()

# Sort chronologically within each visit
tableau_df = tableau_df.sort_values(
    ["visitor_id", "visit_id", "date_time"]
).reset_index(drop=True)


# --------------------------------------------
# KPI 1 - COMPLETION
# --------------------------------------------

# Clients who reached confirm at least once
completed_clients = (
    tableau_df.loc[
        tableau_df["process_step"] == "confirm",
        "client_id"
    ]
    .drop_duplicates()
)

tableau_df["completed"] = (
    tableau_df["client_id"].isin(completed_clients)
).astype(int)


# --------------------------------------------
# KPI 2 - TIME SPENT PER STEP
# --------------------------------------------

# Next timestamp within the SAME visit
tableau_df["next_date_time"] = (
    tableau_df
    .groupby(["visitor_id", "visit_id"])["date_time"]
    .shift(-1)
)

tableau_df["duration_seconds"] = (
    tableau_df["next_date_time"] - tableau_df["date_time"]
).dt.total_seconds()

# Negative durations are invalid
tableau_df.loc[
    tableau_df["duration_seconds"] < 0,
    "duration_seconds"
] = np.nan

# Keep your existing 30-minute rule
tableau_df["duration_seconds_filtered"] = (
    tableau_df["duration_seconds"]
    .where(tableau_df["duration_seconds"] <= 1800)
)


# --------------------------------------------
# KPI 3 - ERROR RATE / BACKWARD TRANSITIONS
# --------------------------------------------

step_map = {
    "start": 0,
    "step_1": 1,
    "step_2": 2,
    "step_3": 3,
    "confirm": 4
}

tableau_df["step_num"] = (
    tableau_df["process_step"].map(step_map)
)

tableau_df["next_step"] = (
    tableau_df
    .groupby(["visitor_id", "visit_id"])["process_step"]
    .shift(-1)
)

tableau_df["next_step_num"] = (
    tableau_df["next_step"].map(step_map)
)

# NaN for the final event of a visit.
# Tableau AVG(is_backward) will therefore use transitions only.
tableau_df["is_backward"] = np.where(
    tableau_df["next_step_num"].notna(),
    (
        tableau_df["next_step_num"]
        < tableau_df["step_num"]
    ).astype(int),
    np.nan
)


# --------------------------------------------
# ADD CLIENT DEMOGRAPHICS
# --------------------------------------------

client_columns = [
    "client_id",
    "client_tenure_year",
    "client_tenure_months",
    "client_age",
    "gender",
    "number_of_accounts",
    "balance",
    "calls_last_6_months",
    "logons_last_6_months"
]

client_info = (
    clients_df[client_columns]
    .drop_duplicates("client_id")
)

tableau_df = tableau_df.merge(
    client_info,
    on="client_id",
    how="left"
)


# --------------------------------------------
# USEFUL TABLEAU SEGMENTS
# --------------------------------------------

tableau_df["age_group"] = pd.cut(
    tableau_df["client_age"],
    bins=[0, 30, 45, 60, np.inf],
    labels=["≤30", "31-45", "46-60", "60+"]
)

tableau_df["tenure_group"] = pd.cut(
    tableau_df["client_tenure_year"],
    bins=[-1, 5, 10, 20, np.inf],
    labels=["0-5", "6-10", "11-20", "20+"]
)

tableau_df["balance_group"] = pd.qcut(
    tableau_df["balance"],
    q=4,
    labels=["Q1 - Lower", "Q2", "Q3", "Q4 - Higher"],
    duplicates="drop"
)


print("Rows:", len(tableau_df))
print("Unique clients:", tableau_df["client_id"].nunique())
print("Columns:", tableau_df.columns.tolist())


# --- Notebook cell 234 ---
## Tableau export — verify and write out the event-level tableau_df built above

# 1. Verify tableau_df exists and has one row per event (not per client —
#    this is the rich event-level dataset built in the previous cell, which
#    must NOT be overwritten with a client-level copy or the KPI columns
#    (completed, duration_seconds, is_backward, etc.) are lost)
print("tableau_df shape:", tableau_df.shape)
print("Unique clients:", tableau_df["client_id"].nunique())

# 2. Verify Test / Control
print("\nVariation counts (rows):")
print(tableau_df["variation"].value_counts(dropna=False))

# 3. Verify columns
print("\nColumns:")
print(tableau_df.columns.tolist())

# 4. Verify completion rate can be reproduced
if "completed" in tableau_df.columns:
    print("\nCompletion rate (unique clients):")
    print(
        tableau_df.groupby("variation")
        .apply(
            lambda x: x.loc[x["completed"] == 1, "client_id"].nunique() / x["client_id"].nunique(),
            include_groups=False
        )
    )

# 5. Check missing values in the key KPI columns actually present in tableau_df
check_cols = [
    c for c in [
        "completed",
        "duration_seconds",
        "duration_seconds_filtered",
        "is_backward"
    ]
    if c in tableau_df.columns
]

if check_cols:
    print("\nMissing KPI values:")
    print(tableau_df[check_cols].isna().sum())

# 6. Export for Tableau
tableau_df.to_csv(
    "vanguard_tableau_data.csv",
    index=False
)
print("\nExport complete: vanguard_tableau_data.csv")


# --- Notebook cell 235 ---
# Verify dta

print("COMPLETION RATE")
print(
    tableau_df
    .groupby("variation")
    .apply(
        lambda x:
        x.loc[x["completed"] == 1, "client_id"].nunique()
        / x["client_id"].nunique(),
        include_groups=False
    )
)

print("\nMEDIAN TIME PER STEP")
print(
    tableau_df
    .groupby(["variation", "process_step"])
    ["duration_seconds_filtered"]
    .median()
)

print("\nBACKWARD TRANSITION RATE")
print(
    tableau_df
    .groupby("variation")["is_backward"]
    .mean()
)

print("\nMISSING DEMOGRAPHICS")
print(
    tableau_df[
        ["client_age", "gender", "client_tenure_year", "balance"]
    ].isna().sum()
)


# --- Notebook cell 237 ---
# --------------------------------------------
# EXPORT TO CSV FOR TABLEAU
# --------------------------------------------
tableau_df.to_csv("tableau_export.csv", index=False)

print("Exported:", tableau_df.shape[0], "rows and", tableau_df.shape[1], "columns")

# --- Final notes ---
# The notebook also contains exploratory plotting and a Streamlit app skeleton.
# Those notebook-only presentation components are intentionally not included here.
#
# The final Tableau-ready event-level export is written as:
#     tableau_export.csv
#
# Expected primary analysis conclusions from the final updated notebook sections:
# H1: Test completion is significantly higher than Control.
# H2: Observed relative uplift is above 5%, but the threshold is not statistically confirmed.
# H3: Start -> Step 1 improves significantly; Step 1 -> Step 2 worsens significantly;
#     later transition differences are not significant after Bonferroni correction.
