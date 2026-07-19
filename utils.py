import pandas as pd
import streamlit as st

# -------------------------
# Dataset Loading And Cleaning
# -------------------------

@st.cache_data
def load_data():
        
    """
    Load, clean, and cache the OWID energy dataset.

    Returns:
        A cleaned pandas DataFrame containing energy data from 1990 onwards.
    """

    df = pd.read_csv("owid-energy-data.csv")
    df = df[df["year"] >= 1990]

    numeric_columns = df.select_dtypes(include="number").columns
    non_numeric_columns = df.select_dtypes(exclude="number").columns

    df[non_numeric_columns] = (
    df[non_numeric_columns]
    .fillna("unknown")
    .astype(str)
    .apply(lambda col: col.str.strip().str.lower())
    )

    df[numeric_columns] = (
        df[numeric_columns]
        .fillna(0)
        .astype(float)
    )

    df = df.drop_duplicates()

    df = df[
        (df["iso_code"] != "nan")
        &
        (df["iso_code"] != "unknown")
    ]

    return df

# -------------------------
# Country Comparison
# -------------------------

def compare_countries(df, country_1, country_2, min_year, metrics_list):

    """
    Return a merged dataframe containing the selected metrics
    for two countries over the specified time period.
    """
        
    c1 = country_1.strip().lower()
    c2 = country_2.strip().lower()

    columns_to_extract = ['year'] + metrics_list

    df_c1 = df[(df['country'] == c1) & (df['year'] >= min_year)][columns_to_extract]
    df_c2 = df[(df['country'] == c2) & (df['year'] >= min_year)][columns_to_extract]

    merged_df = pd.merge(
        df_c1, 
        df_c2, 
        on='year', 
        how='inner', 
        suffixes=(f'_{c1}', f'_{c2}')
    )
    
    return merged_df