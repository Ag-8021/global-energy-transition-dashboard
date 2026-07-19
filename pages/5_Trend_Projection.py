import streamlit as st
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

from utils import load_data
from constants import METRIC_DISPLAY_NAMES

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Trend Projection",
    layout="wide"
)

# -------------------------
# Load Dataset
# -------------------------

df = load_data()

# -------------------------
# Page Title
# -------------------------

st.title("Energy Trend Projection")
st.divider()

# -------------------------
# Projection Controls
# -------------------------

col1, col2 = st.columns(2)

with col1:
    available_countries = sorted(df["country"].unique())
    default_c1 = "india"

    selected_country = st.selectbox(
        "Select Country",
        available_countries,
        index=available_countries.index(default_c1),
        format_func=lambda x: x.title()
    )

with col2:
    selected_metric = st.selectbox(
        "Select Metric",
        list(METRIC_DISPLAY_NAMES.keys()),
        format_func=lambda x: METRIC_DISPLAY_NAMES[x]
    )

st.divider()

# -------------------------
# Filter Country Data
# -------------------------

country_df = df[df["country"] == selected_country]
country_df = country_df[country_df[selected_metric] > 0]

if country_df.empty:
    st.warning(
        f"No data available for {selected_country.title()} for this metric."
    )
    st.stop()

# -------------------------
# Forecast Horizon
# -------------------------

forecast_until = st.slider(
    "Forecast Until",
    int(country_df["year"].max()) + 1,
    2050,
    2035
)

future_years = np.arange(
    country_df["year"].max() + 1,
    forecast_until + 1
).reshape(-1, 1)

st.divider()

# -------------------------
# Train Linear Regression Model
# -------------------------

X = country_df["year"].values.reshape(-1, 1)
y = country_df[selected_metric].values

model = LinearRegression()
model.fit(X, y)

future_predictions = model.predict(future_years)

# -------------------------
# Create Projection Figure
# -------------------------

fig = go.Figure()

# Historical Trend
fig.add_trace(
    go.Scatter(
        x=country_df["year"],
        y=country_df[selected_metric],
        mode="lines",
        name="Historical",
        line=dict(
            color="blue",
            width=3
        )
    )
)

# Forecast Trend
forecast_x = np.concatenate(
    ([country_df["year"].iloc[-1]], future_years.flatten())
)

forecast_y = np.concatenate(
    ([country_df[selected_metric].iloc[-1]], future_predictions)
)

fig.add_trace(
    go.Scatter(
        x=forecast_x,
        y=forecast_y,
        mode="lines",
        name="Forecast",
        line=dict(
            color="orange",
            width=3,
            dash="dash"
        )
    )
)

# -------------------------
# Figure Layout
# -------------------------

fig.update_layout(
    title=(
        f"{selected_country.title()} - "
        f"{METRIC_DISPLAY_NAMES[selected_metric]} Forecast"
    ),
    xaxis_title="Year",
    yaxis_title=METRIC_DISPLAY_NAMES[selected_metric],
    hovermode="x unified",
    template="plotly_white",
    legend_title="Data",
    height=550,
    transition_duration=500
)

# -------------------------
# Display Projection
# -------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------
# Forecast Disclaimer
# -------------------------

st.info(
    "Forecasts are generated using a simple Linear Regression model based on historical trends."
)