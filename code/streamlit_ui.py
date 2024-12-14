from census_call import get_census_data as gcd
import streamlit as st


api_key = st.text_input("Enter your Census API key: ")


if api_key:
    df = gcd(api_key, "B19013_001E", 2017)
    st.dataframe(df)


