import numpy as np
import pandas as pd

from constants import POSITIVE_METRICS

# -------------------------
# Green Score Calculation
# -------------------------

def calculate_green_score(country_df, target_year):

    """
    Calculate the Green Score, a custom sustainability index (0-100)
    based on renewable electricity share, coal reduction, solar and wind
    generation, and carbon intensity.
    """

    year_data = country_df[country_df["year"] == target_year]

    if year_data.empty:
        return 0.0

    row = year_data.iloc[0]

    # --- Renewable Share (0-50) ---

    renewable_share = row["renewables_share_elec"]
    renewable_score = min(renewable_share / 100 * 50, 50)

    # --- Coal Reduction (0-20) ---

    max_coal = country_df["coal_electricity"].max()

    if max_coal > 0:
        coal_ratio = row["coal_electricity"] / max_coal
        coal_score = (1 - coal_ratio) * 20
    else:
        coal_score = 20

    # --- Solar Progress (0-10) ---

    max_solar = country_df["solar_electricity"].max()

    if max_solar > 0:
        solar_score = (
            row["solar_electricity"] /
            max_solar
        ) * 10
    else:
        solar_score = 0

    # --- Wind Progress (0-10) ---

    max_wind = country_df["wind_electricity"].max()

    if max_wind > 0:
        wind_score = (
            row["wind_electricity"] /
            max_wind
        ) * 10
    else:
        wind_score = 0

    # --- Carbon Intensity (0-10) ---

    max_carbon = country_df["carbon_intensity_elec"].max()

    if max_carbon > 0:
        carbon_score = (
            1 -
            row["carbon_intensity_elec"] /
            max_carbon
        ) * 10
    else:
        carbon_score = 10

    carbon_score = max(0, carbon_score)

    green_score = (
        renewable_score +
        coal_score +
        solar_score +
        wind_score +
        carbon_score
    )

    return round(min(green_score, 100), 2)

# -------------------------
# World Ranking Calculation
# -------------------------

def calculate_world_rank(df, country, metric):

    """
    Return the world rank of a country for the selected metric
    using the latest available data for that country.

    Returns:
        (rank, year) if available, otherwise (None, year).
    """

    # --- Filtering Data Of Selected Country ---

    country_df = df[df["country"] == country]

    if country_df.empty:
        return None, None

    latest_year = int(country_df["year"].max())

    latest_row = country_df[country_df["year"] == latest_year]

    # --- Handling Missing Data ---

    if latest_row.empty:
        return None, latest_year

    if metric not in latest_row.columns:
        return None, latest_year
    
    value = latest_row[metric].iloc[0]

    if pd.isna(value) or value <= 0:
        return None, latest_year
    
    # --- Ranking By Metric ---

    ascending = metric not in POSITIVE_METRICS

    ranking_df = (
        df[
            (df["year"] == latest_year)
            &
            (df[metric] > 0)
        ]
        .sort_values(
            by=metric,
            ascending=ascending
        )
        .reset_index(drop=True)
    )

    ranking_df["rank"] = ranking_df.index + 1

    result = ranking_df.loc[
        ranking_df["country"] == country,
        "rank"
    ]

    if result.empty:
        return None, latest_year

    return int(result.iloc[0]), latest_year