from playwright.sync_api import Playwright, sync_playwright
from time import sleep
from census import Census
import requests
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt



shapefile_path = "path_to_shapefile/tl_2021_36_tract.shp"
gdf = gpd.read_file(shapefile_path)

# Replace 'your_api_key' with your actual Census API key
API_KEY = "4ca091407dc4c018ee7aa725fe60c9362b0f86ba"
c = Census(API_KEY, )


data = c.acs5.state_county_tract(
    ("NAME", "B19013_001E"),  # Median Household Income
    state_fips="36",          # New York State
    county_fips="067",        # Onondaga County
    tract="*",
    with_geo = True
)
print(data)
df = pd.DataFrame(data)

# Extract tract number from the 'NAME' field
df["Tract_Number"] = df["NAME"].str.extract(r"Census Tract (\d+\.?\d*)").astype(float)

# Filter for tracts with numbers <= 61.03
syracuse_data = df[df["Tract_Number"] <= 61.03]
st.dataframe(syracuse_data)