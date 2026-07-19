import streamlit as st

from metrics import calculate_green_score
from utils import load_data

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Green Score Comparison",
    layout="wide"
)

# -------------------------
# Load Dataset
# -------------------------

df = load_data()

# -------------------------
# Page Title
# -------------------------

st.title("Green Score Comparison")
st.markdown(
    "Evaluate and compare countries using Green Score - a custom sustainability index."
)

# -------------------------
# Green Score Explanation
# -------------------------

with st.expander(
    "How is the Green Score calculated?",
    expanded=True
):

    st.markdown("""
The **Green Score** is a custom sustainability index developed for this dashboard to estimate a country's progress towards cleaner electricity generation.

It is calculated using:

- **Renewable Electricity Share** - Countries generating a larger proportion of electricity from renewable sources receive higher scores.
- **Reduction in Coal-Based Electricity** - Countries that have reduced their dependence on coal relative to their historical levels receive additional points.

The score ranges from **0 to 100**, where higher values indicate stronger progress towards a cleaner and more sustainable electricity mix.

**Note:** This is a custom metric created for comparative analysis within this project and is not an official sustainability index.
""")

st.divider()

# -------------------------
# Country Selection
# -------------------------

available_countries = sorted(df["country"].unique())

default_c1 = (
    "india"
    if "india" in available_countries
    else available_countries[0]
)

default_c2 = (
    "china"
    if "china" in available_countries
    else available_countries[0]
)

country_1 = st.selectbox(
    "Select Country 1",
    available_countries,
    index=available_countries.index(default_c1),
    format_func=lambda x: x.title()
)

country_2 = st.selectbox(
    "Select Country 2",
    available_countries,
    index=available_countries.index(default_c2),
    format_func=lambda x: x.title()
)

# -------------------------
# Year Selection
# -------------------------

min_dataset_year = 1990
max_dataset_year = int(df["year"].max())

selected_year = st.slider(
    "Select Year",
    min_dataset_year,
    max_dataset_year,
    max_dataset_year
)

st.divider()

# -------------------------
# Green Score Comparison
# -------------------------

st.subheader(f"Green Score Comparison ({selected_year})")
st.caption("Calculated using data from the selected year.")

df_c1 = df[df["country"] == country_1]
df_c2 = df[df["country"] == country_2]

score_1 = calculate_green_score(
    df_c1,
    selected_year
)

score_2 = calculate_green_score(
    df_c2,
    selected_year
)

metric_col1, metric_col2 = st.columns(2)

metric_col1.metric(
    label=f"{country_1.title()} Green Score",
    value=f"{score_1:.2f} / 100"
)

metric_col2.metric(
    label=f"{country_2.title()} Green Score",
    value=f"{score_2:.2f} / 100"
)

st.divider()

# -------------------------
# Global Benchmark
# -------------------------

st.markdown("## Global Benchmark")

if st.checkbox(
    "Show the highest Green Score for the selected year"
):

    with st.spinner("Calculating..."):

        max_score = 0.0
        max_country = "None"

        for individual_country in df["country"].unique():

            country_df = df[
                df["country"] == individual_country
            ]

            country_green_score = calculate_green_score(
                country_df,
                selected_year
            )

            if country_green_score > max_score:
                max_score = country_green_score
                max_country = individual_country

        st.success(
            f"**Highest Green Score:** "
            f"{max_country.title()} "
            f"({max_score:.2f}/100)"
        )