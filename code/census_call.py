from census import Census
import pandas as pd
import geopandas as gpd

def get_census_tables(api_key, year=2022):
    census = Census(api_key)
    variables = census.acs5.tables(year=year)
    return variables


def get_census_data(api_key, var, year=2022):
    census = Census(api_key, year=year)
    data = census.acs5.state_county_tract(
        ("NAME", var),
        state_fips="36",
        county_fips="067",
        tract="*"
    )

    df = pd.DataFrame(data)
    df['NAME'] = df['NAME'].replace("Census Tract 44, Onondaga County, New York", "Census Tract 44.01, Onondaga County, New York")
    df['tract_number'] = df['NAME'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    # reassign tract 44 to 44.01
    df['tract'] = df['tract'].replace("004400", "004401")
    df['GEOID'] = df['state'] + df['county'] + df['tract']
    # df['GEOID'] = df['GEOID'].replace("36067004400", "36067004401")
    print(df[df['tract_number'] == 44.01][['GEOID']])
    syracuse_df = df[df['tract_number'] <= 61.03]
    return syracuse_df

def merge_with_shapefile(census_df):
    # Read the shapefile
    gdf = gpd.read_file("code/data/census_tracts/tl_2024_36_tract.shp")
    # Merge the shapefile with the census data
    gdf_merge = gdf.merge(census_df, on="GEOID", how="right")
    return gdf_merge


if __name__ == "__main__":
    api_key = input("Enter your Census API key: ")
    df = get_census_data(api_key, "B19013_001E")
    gdf = gpd.read_file("code/data/census_tracts/tl_2024_36_tract.shp")    
    #write to cache
    merge_df = merge_with_shapefile(df)

