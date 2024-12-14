from census_call import get_census_data
from census_call import get_census_tables
from census_call import merge_with_shapefile

import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit_folium as sf


api_key = st.text_input("Enter your Census API key: ")



if api_key:
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select year", [2017, 2018, 2019, 2020, 2021, 2022])
    with col2:
        metric = st.text_input("Enter metric ID", "B19013_001E")

    # Initialize session state for the button
    if 'get_vars' not in st.session_state:
        st.session_state.get_vars = False

    # Button to view census tables
    if st.button("View Census Tables for selected year"):
        st.session_state.get_vars = True

    if st.session_state.get_vars:
        tables = get_census_tables(api_key, year)
        st.dataframe(tables)
    
    # Initialize session state for the button
    if 'load_map' not in st.session_state:
        st.session_state.load_map = False

    # Button to load the map
    if st.button("Load map"):
        st.session_state.load_map = True

    if st.session_state.load_map:
        df = get_census_data(api_key, metric, year)
        gdf = merge_with_shapefile(df)
        st.dataframe(gdf)

        # Create a base Folium map
        m = folium.Map(location=[43.088947, -76.154480], zoom_start=12)  # Coordinates for Syracuse, NY

        # Define a style function for the polygons
        def style_function(feature):
            return {
                'color': 'black',  # Outline color
                'weight': 1,      # Outline width
                'fillOpacity': 0
            }

        # Create a choropleth map
        folium.Choropleth(
            geo_data=gdf,
            name='choropleth',
            data=gdf,
            columns=['GEOID', metric],
            key_on='feature.properties.GEOID',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Median Household Income'
        ).add_to(m)

        # Add GeoDataFrame polygons to the map with custom styles
        folium.GeoJson(
            data=gdf,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(fields=['tract_number', metric], aliases=['Tract:', 'Median Household Income:'])
        ).add_to(m)

        # Add tract labels
        for _, row in gdf.iterrows():
            centroid = row['geometry'].centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(html=f"""<div style="font-size: 12px; color: black;">{row['tract_number']}</div>""")
            ).add_to(m)

        # Display the Folium map in Streamlit
        st.title("Polygon Layer Map")
        st_folium(m, width=700, height=500)
