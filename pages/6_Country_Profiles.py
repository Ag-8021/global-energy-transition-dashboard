import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data
from constants import ENERGY_SOURCE_NAMES
from metrics import calculate_green_score
from metrics import calculate_world_rank

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Country Profiles",
    layout="wide"
)

# -------------------------
# Load Dataset
# -------------------------

df = load_data()

# -------------------------
# Country Selection
# -------------------------

st.title("Country Energy Profiles")
st.divider()

available_countries = sorted(df["country"].unique())

selected_country = st.selectbox(
    "Select Country",
    available_countries,
    index=available_countries.index("india"),
    format_func=lambda x: x.title()
)

country_df = df[df["country"] == selected_country]

latest_year = int(country_df["year"].max())
latest_row = country_df[country_df["year"] == latest_year].iloc[0]

st.divider()

st.title(selected_country.title())

st.divider()

col1, col2 = st.columns(2)

# -------------------------
# Green Score
# -------------------------

with col1:

    st.markdown("## Green Score")

    green_score = calculate_green_score(
        country_df,
        latest_year
    )

    st.progress(green_score / 100)

    st.markdown(
        f"#### {green_score:.2f}/100"
    )

# -------------------------
# World Rank
# -------------------------

with col2:

    rank, rank_year = calculate_world_rank(
        df,
        selected_country,
        "renewables_share_elec"
    )

    st.markdown("## World Rank")

    if rank is None:
        st.warning("No ranking available.")
    else:
        st.markdown(f"#### #{rank}")

st.caption(f"Based on {rank_year} data")

st.divider()

# -------------------------
# Latest Statistics
# -------------------------

st.markdown("## Latest Statistics")

# -------------------------
# Metric Card Helper
# -------------------------

def metric_card(title, metric, unit):

    value = latest_row.get(metric, 0)

    rank, _ = calculate_world_rank(
        df,
        selected_country,
        metric
    )

    if pd.isna(value):
        value = 0

    if rank is None:

        st.metric(
            title,
            f"{value:.2f} {unit}"
        )

    else:

        st.metric(
            title,
            f"{value:.2f} {unit}",
            f"Rank #{rank}"
        )

col1, col2 = st.columns(2)

with col1:
    metric_card(
        "Renewable Share",
        "renewables_share_elec",
        "%"
    )

with col2:
    metric_card(
        "Solar Generation",
        "solar_electricity",
        "TWh"
    )

col1, col2 = st.columns(2)

with col1:
    metric_card(
        "Wind Generation",
        "wind_electricity",
        "TWh"
    )

with col2:
    metric_card(
        "Coal Generation",
        "coal_electricity",
        "TWh"
    )

st.caption(f"Based on {latest_year} data")

st.divider()

# -------------------------
# Renewable Share Trend
# -------------------------

trend_df = country_df[
    ["year", "renewables_share_elec"]
].copy()

fig = px.line(
    trend_df,
    x="year",
    y="renewables_share_elec",
    markers=True,
    title="Renewable Electricity Share Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Renewable Share (%)",
    height=320,
    showlegend=False,
    transition_duration=500
)

fig.update_traces(
    line_width=3,
    hovertemplate=
    "<b>Year:</b> %{x}<br>"
    "<b>Renewable Share:</b> %{y:.2f}%<extra></extra>"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------
# Energy Mix Summary
# -------------------------

st.subheader(f"Electricity Generation Mix ({latest_year})")

sources = []
values = []

for column, display_name in ENERGY_SOURCE_NAMES.items():

    if column not in latest_row.index:
        continue

    value = latest_row[column]

    if pd.isna(value):
        continue

    if value <= 0:
        continue

    sources.append(display_name)
    values.append(value)

if len(values) == 0:

    st.info("No electricity generation data available.")

else:

    pie_df = pd.DataFrame(
        {
            "Source": sources,
            "Generation (TWh)": values
        }
    )

    primary_source = pie_df.loc[
        pie_df["Generation (TWh)"].idxmax()
    ]

    total_generation = pie_df["Generation (TWh)"].sum()

    share = (
        primary_source["Generation (TWh)"]
        / total_generation
    ) * 100

    col1, col2 = st.columns([1, 2])

    # -------------------------
    # Primary Energy Source
    # -------------------------

    with col1:

        st.metric(
            "Primary Electricity Source",
            primary_source["Source"],
            f"{share:.1f}% of generation"
        )

    # -------------------------
    # Energy Mix Pie Chart
    # -------------------------

    with col2:

        fig = px.pie(
            pie_df,
            names="Source",
            values="Generation (TWh)",
            title=" "
        )

        fig.update_traces(
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "%{value:.2f} TWh"
                "<br>%{percent}"
                "<extra></extra>"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )