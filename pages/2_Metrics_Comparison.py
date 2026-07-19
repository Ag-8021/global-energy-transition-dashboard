import streamlit as st
import plotly.express as px

from utils import load_data, compare_countries
from constants import METRIC_DISPLAY_NAMES

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Metrics Comparison",
    layout="wide"
)

# -------------------------
# Load Dataset
# -------------------------

df = load_data()

# -------------------------
# Page Title
# -------------------------

st.title("Metrics Comparison")
st.markdown("Compare energy metrics and country performance over time.")

# -------------------------
# Country Selection
# -------------------------

available_countries = sorted(df["country"].unique())

default_c1 = "india" if "india" in available_countries else available_countries[0]
default_c2 = "china" if "china" in available_countries else available_countries[0]

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
# Year Range Selection
# -------------------------

min_dataset_year = 1990
max_dataset_year = int(df["year"].max())

selected_years = st.slider(
    "Select Year Range",
    min_dataset_year,
    max_dataset_year,
    [2010, 2020]
)

start_year, end_year = selected_years

# -------------------------
# Metric Selection
# -------------------------

available_metrics = list(METRIC_DISPLAY_NAMES.keys())
default_index = available_metrics.index("renewables_share_elec")

chosen_metric = st.selectbox(
    "Select Metric to Plot",
    options=available_metrics,
    index=default_index,
    format_func=lambda x: METRIC_DISPLAY_NAMES[x]
)

st.divider()

# -------------------------
# Comparison Visualization
# -------------------------

if chosen_metric:

    comparison_data = compare_countries(
        df,
        country_1,
        country_2,
        start_year,
        [chosen_metric]
    )

    st.subheader(
        f"Timeline Comparison: {country_1.title()} vs {country_2.title()}"
    )

    col1_name = f"{chosen_metric}_{country_1.lower()}"
    col2_name = f"{chosen_metric}_{country_2.lower()}"

    if (
        col1_name in comparison_data.columns
        and
        col2_name in comparison_data.columns
    ):

        graph_filtered_data = comparison_data[
            comparison_data["year"] <= end_year
        ]

        legend_labels = {
            col1_name: country_1.title(),
            col2_name: country_2.title()
        }

        fig = px.line(
            graph_filtered_data,
            x="year",
            y=[col1_name, col2_name],
            labels={
                "value": METRIC_DISPLAY_NAMES[chosen_metric],
                "variable": "Country"
            },
            title=(
                f"{METRIC_DISPLAY_NAMES[chosen_metric]} "
                f"({start_year} - {end_year})"
            )
        )

        fig.for_each_trace(
            lambda t: t.update(
                name=legend_labels.get(t.name, t.name)
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(
            "Insufficient parallel chronological data found to plot this comparison."
        )

else:
    st.warning(
        "Please select a metric to visualize."
    )