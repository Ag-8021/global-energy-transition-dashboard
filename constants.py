# Display Names Used Throughout The UI For Energy Metrics
METRIC_DISPLAY_NAMES = {
    'renewables_share_elec': 'Renewable Share of Electricity Generation (%)',
    'coal_electricity': 'Coal Electricity Generation (TWh)',
    'solar_electricity': 'Solar Electricity Generation (TWh)',
    'wind_electricity': 'Wind Electricity Generation (TWh)',
    'carbon_intensity_elec': 'Carbon Intensity of Electricity (gCO2/kWh)'
}

# Metrics Where Higher Values Indicate Better Environmental Performance
POSITIVE_METRICS = {
    "renewables_share_elec",
    "solar_electricity",
    "wind_electricity",
}

# Display Names For Electricity Generation Sources Used In Charts
ENERGY_SOURCE_NAMES = {
    "coal_electricity": "Coal",
    "gas_electricity": "Natural Gas",
    "oil_electricity": "Oil",
    "solar_electricity": "Solar",
    "wind_electricity": "Wind",
    "hydro_electricity": "Hydroelectric",
    "nuclear_electricity": "Nuclear",
    "biofuel_electricity": "Biofuel",
    "other_renewable_electricity": "Other Renewables"
}