from playwright.sync_api import Playwright, sync_playwright
from time import sleep
from census import Census
import requests
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt



shapefile_path = "path_to_shapefile/tl_2021_36_tract.shp"
gdf = gpd.read_file("code/data/census_tracts/tl_2024_36_tract.shp")
# Replace 'your_api_key' with your actual Census API key
API_KEY = "4ca091407dc4c018ee7aa725fe60c9362b0f86ba"
c = Census(API_KEY)


data = c.acs5.state_county_tract(
    ("NAME", "B19013_001E"),  # Median Household Income
    state_fips="36",          # New York State
    county_fips="067",        # Onondaga County
    tract="*",
)

df = pd.DataFrame(data)
df['tract_number'] = df['NAME'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
syracuse_df = df[df['tract_number'] <= 61.03]
print("Syracuse CENSUS")
print(syracuse_df.head(3))

merge_df = syracuse_df.merge(gdf, left_on="tract", right_on="TRACTCE")
print("Merged")
print(merge_df.head(3))

merge_gdf = gpd.GeoDataFrame(merge_df, geometry='geometry')


# Streamlit setup
st.title('Syracuse Census Tracts - Median Household Income')

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))
merge_gdf.plot(column='B19013_001E', cmap='viridis', legend=True, ax=ax)
plt.title('Median Household Income in Syracuse Tracts')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot in Streamlit
st.pyplot(fig)