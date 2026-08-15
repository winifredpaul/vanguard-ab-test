import pandas as pd
import streamlit as st

# clients_df should be exported from the notebook first, e.g.:
# clients_df.to_csv("clients_df.csv", index=False)
df = pd.read_csv("clients_df.csv")

st.title("Vanguard A/B Experiment Dashboard")

variation = st.selectbox("Select variation", ["Control", "Test"])

filtered = df[df["variation"] == variation]

completion_rate = (filtered["furthest_step_reached"] == "confirm").mean()
st.metric("Completion Rate", f"{completion_rate:.2%}")

st.subheader("Completion Rate by Age Group")
age_completion = (
    filtered.assign(
        age_group=pd.cut(
            filtered["client_age"],
            bins=[18, 30, 45, 60, 100],
            labels=["18–30", "31–45", "46–60", "60+"],
            include_lowest=True
        )
    )
    .groupby("age_group")["furthest_step_reached"]
    .apply(lambda x: (x == "confirm").mean())
    .reset_index(name="completion_rate")
)

st.bar_chart(age_completion.set_index("age_group")["completion_rate"])
