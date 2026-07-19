import streamlit as st
import plotly.express as px

from constants import METRIC_DISPLAY_NAMES
from constants import POSITIVE_METRICS
from utils import load_data

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="World Leaderboard",
    layout="wide"
)

st.title("Global Energy Rankings")
st.divider()

# -------------------------
# Load Dataset
# -------------------------

df = load_data()

# -------------------------
# User Controls
# -------------------------

col1, col2 = st.columns(2)

with col1:
    selected_year = st.slider(
        "Select Year",
        int(df["year"].min()),
        int(df["year"].max()),
        int(df["year"].max())
    )

with col2:
    selected_metric = st.selectbox(
        "Select Metric",
        list(METRIC_DISPLAY_NAMES.keys()),
        format_func=lambda x: METRIC_DISPLAY_NAMES[x]
    )

st.divider()

# -------------------------
# Generate Leaderboard
# -------------------------

ascending = selected_metric not in POSITIVE_METRICS

year_df = df[df["year"] == selected_year]

valid_df = year_df[year_df[selected_metric] > 0]

ranking_df = (
    valid_df[["country", selected_metric]]
    .sort_values(
        by=selected_metric,
        ascending=ascending
    )
    .reset_index(drop=True)
)

ranking_df["country"] = ranking_df["country"].str.title()

# -------------------------
# Leaderboard Visualization
# -------------------------

fig = px.bar(

    ranking_df.head(10),

    x=selected_metric,

    y="country",

    orientation="h",

    text=selected_metric,

    title=f"Top 10 Countries by {METRIC_DISPLAY_NAMES[selected_metric]}",

    labels={
        selected_metric: METRIC_DISPLAY_NAMES[selected_metric],
        "country": "Country"
    }
)

fig.update_layout(
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(
    fig,
    use_container_width=True
)