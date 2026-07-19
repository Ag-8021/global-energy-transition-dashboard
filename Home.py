import streamlit as st
from constants import METRIC_DISPLAY_NAMES

from utils import load_data
from metrics import calculate_green_score

# ----------------------------
# Page Configuration & Title
# ----------------------------

st.set_page_config(page_title="Global Energy Transition Dashboard", layout="wide")

st.markdown(
    """
    <h1 style='text-align:center;'>
    Global Energy Transition Dashboard
    </h1>
    <p style='text-align:center; font-size:20px;'>
    Tracking the world's shift towards cleaner energy through data-driven insights.
    </p>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Button Styling (CSS)
# ----------------------------

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

# ----------------------------
# Navigation / Action Button
# ----------------------------

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Explore Global Energy Rankings →"):
        st.switch_page("pages/1_World_Leaderboard.py")
with col2:
    if st.button("Explore World Energy Map →"):
        st.switch_page("pages/4_World_Map.py")
with col3:
    if st.button("Explore Energy Trend Projections →"):
        st.switch_page("pages/5_Trend_Projection.py")

st.divider()

# ----------------------------
# Load & Setup Data
# ----------------------------

df = load_data()
latest_year = int(df['year'].max())
latest_data = df[df['year'] == latest_year]

# ----------------------------
# Core KPI Metrics
# ----------------------------

col1, col2, col3, col4 = st.columns([1, 1.5, 1, 1])

col1.metric("Countries Analysed", "190 +")
col2.metric("Years Covered", f"1990-{latest_year}")
col3.metric("Energy Indicators", len(METRIC_DISPLAY_NAMES))
col4.metric("Data Source", "OWID")

st.divider()

# ----------------------------
# Latest Global Insights
# ----------------------------

st.markdown("<h2 style='text-align:center;'>Latest Global Insights</h2>", unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns(3)

# --- Highest Renewable Share ---
with col_1:
    highest_renewable = latest_data.loc[latest_data["renewables_share_elec"].idxmax()]
    renewable_country = highest_renewable["country"].title()
    renewable_value = highest_renewable["renewables_share_elec"]
    st.metric(
        "Renewability Leader",
        renewable_country,
        f"{renewable_value:.1f}%"
    )

# --- Highest Green Score ---
with col_2:
    max_score = 0.0
    max_country = 'None'
    
    grouped_df = df.groupby('country')
    
    for country, country_df in grouped_df:
        country_green_score = calculate_green_score(country_df, latest_year)
        if country_green_score > max_score:
            max_score = country_green_score
            max_country = country

    st.metric(
         "Greenest Country",
         max_country.title(),
         f"{max_score:.1f}" if isinstance(max_score, (int, float)) else max_score
    ) 

# --- Largest Solar Producer ---

with col_3:

    highest_solar = latest_data.loc[
        latest_data["solar_electricity"].idxmax()
    ]

    solar_country = highest_solar["country"].title()
    solar_value = highest_solar["solar_electricity"]

    st.metric(
        "Largest Solar Energy Producer",
        solar_country,
        f"{solar_value:.1f} TWh"
    )

st.caption(f"Based on energy data from {latest_year}")