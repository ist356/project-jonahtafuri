from census import Census
import pandas as pd
import geopandas as gpd

def get_census_data(api_key, var, year=2022):
    census = Census(api_key, year=year)
    data = census.acs5.state_county_tract(
        ("NAME", var),
        state_fips="36",
        county_fips="067",
        tract="*"
    )

    df = pd.DataFrame(data)
    df['tract_number'] = df['NAME'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    df['GEOID'] = df['state'] + df['county'] + df['tract']
    syracuse_df = df[df['tract_number'] <= 61.03]
    print("CENSUS:", df['GEOID'].head(3))
    return syracuse_df

def merge_with_shapefile(df):
    # Read the shapefile
    gdf = gpd.read_file("code/data/census_tracts/tl_2024_36_tract.shp")
    print("GDF:", gdf['GEOID'].head(3))
    
    # Merge the DataFrame with the GeoDataFrame
    # merged_gdf = gdf.merge(df, on='tract_number')
    
    return merged_gdf


if __name__ == "__main__":
    api_key = input("Enter your Census API key: ")
    df = get_census_data(api_key, "B19013_001E")
    merged_gdf = merge_with_shapefile(df)
 

