import streamlit as st
import plotly.graph_objects as go

from utils import load_data
from constants import METRIC_DISPLAY_NAMES
from constants import POSITIVE_METRICS

# -------------------------
# Load Dataset
# -------------------------

df = load_data()
df["iso_code"] = df["iso_code"].str.upper()

# -------------------------
# Page Title
# -------------------------

st.title("World Energy Map")
st.markdown("Visualize global energy metrics by country.")

# -------------------------
# Map Controls
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

color_scale = (
    "RdYlGn"
    if selected_metric in POSITIVE_METRICS
    else "RdYlGn_r"
)

# -------------------------
# Filter Data By Year
# -------------------------

map_df = df[df["year"] == selected_year].copy()

# -------------------------
# Build Choropleth Map
# -------------------------

fig = go.Figure(
    go.Choropleth(

        locations=map_df["iso_code"],

        z=map_df[selected_metric],

        locationmode="ISO-3",

        text=map_df["country"].str.title(),

        hovertemplate=(
            "<b>%{text}</b><br>"
            f"{METRIC_DISPLAY_NAMES[selected_metric]}: "
            "%{z:.2f}<br>"
            f"Year: {selected_year}"
            "<extra></extra>"
        ),

        colorscale=color_scale,

        colorbar=dict(

            orientation="h",

            title=dict(
                text=METRIC_DISPLAY_NAMES[selected_metric],
                side="top",
                font=dict(
                    color="black",
                    size=13
                )
            ),

            tickfont=dict(
                color="black"
            ),

            thickness=14,

            len=0.45,

            x=0.5,
            xanchor="center",

            y=-0.02,
            yanchor="top",

            outlinewidth=0
        ),

        marker=dict(
            line=dict(
                color="black",
                width=0.4
            )
        )
    )
)

# -------------------------
# Map Styling
# -------------------------

fig.update_geos(

    projection_type="natural earth",

    projection_scale=1.25,

    center=dict(
        lat=15,
        lon=0
    ),

    showcountries=True,
    countrycolor="black",
    countrywidth=0.6,

    showcoastlines=True,
    coastlinecolor="black",
    coastlinewidth=0.6,

    showland=True,
    landcolor="white",

    showocean=True,
    oceancolor="aliceblue",

    showframe=False,

    bgcolor="white"
)

# -------------------------
# Figure Layout
# -------------------------

fig.update_layout(

    height=650,

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=35
    ),

    paper_bgcolor="white",

    plot_bgcolor="white",

    dragmode=False
)

# -------------------------
# Render Map
# -------------------------

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "scrollZoom": False
    }
)

# -------------------------
# Metric Interpretation
# -------------------------

if selected_metric in POSITIVE_METRICS:
    st.success("Higher values indicate better performance.")
else:
    st.success("Lower values indicate better performance.")

st.divider()

# -------------------------
# Navigation Button Styling
# -------------------------

st.markdown(
    """
    <style>
    div.stButton > button {
        width: 250px;
        height: 50px;
        font-size: 18px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Navigation
# -------------------------

col1, col2, col3 = st.columns(3)

with col2:
    if st.button("Explore Country Energy Profiles →"):
        st.switch_page("pages/6_Country_Profiles.py")