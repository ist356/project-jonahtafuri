from census import Census
import pandas as pd

api_key = input("Enter your Census API key: ")

def get_census_data(api_key, var):
    census = Census(api_key)
    data = census.acs5.state_county_tract(
        ("NAME", var),
        state_fips="36",
        county_fips="067",
        tract="*"
    )

    df = pd.DataFrame(data)
    df['tract_number'] = df['NAME'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    syracuse_df = df[df['tract_number'] <= 61.03]
    return syracuse_df


if __name__ == "__main__":
    df = get_census_data(api_key, "B19013_001E")
    print("Syracuse CENSUS")
    print(df.head(3))