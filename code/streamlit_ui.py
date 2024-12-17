from census_call import get_census_data
from census_call import get_census_tables
from census_call import merge_with_shapefile
import os
import tempfile
import zipfile
import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit_folium as sf
from census import Census
import requests

st.title("Syracuse Census Data Mapper")
api_key = st.text_input("Enter your Census API key: ")

# Initialize session state for the button
if 'get_tables' not in st.session_state:
    st.session_state.get_tables = False


if api_key:
    col1, col2 = st.columns([1,2])
    with col1:
        year = st.selectbox("Select Census Year", [2017, 2018, 2019, 2020, 2021, 2022])
    with col2:
    # Button to view census tables
        st.write("")
        st.write("")
        if st.button("View Census Tables for Selected Year"):
            st.session_state.get_tables = True

    if st.session_state.get_tables:
        tables = get_census_tables(api_key, year)
        st.dataframe(tables)
        # Initialize session state for the button
        # Additional functionality: Viewing variables
        if 'get_vars' not in st.session_state:
            st.session_state.get_vars = False
        st.write("")
        st.markdown(
            "<h5 style='text-align: center;'>For more information on metrics, enter the table name into the text box below</div>", 
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            entry = st.text_input("Enter Table ID to View Metrics:", "B19013")
        with col2:
            st.write("")
            st.write("")
            if st.button("View Metrics for Selected Table"):
                st.session_state.get_vars = True

        if st.session_state.get_vars:
            # Fetch variables from the Census metadata endpoint
            url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                variables = data.get("variables", {})

                # Filter variables for the selected table
                filtered_variables = {
                    var: metadata for var, metadata in variables.items() if var.startswith(f"{entry}_")
                }

                if filtered_variables:
                    # Convert filtered variables to a DataFrame
                    import pandas as pd

                    # Prepare data for the DataFrame
                    df_data = [
                        {"Variable": variable, "Label": metadata["label"]}
                        for variable, metadata in filtered_variables.items()
                    ]
                    df = pd.DataFrame(df_data)

                    # Display as a dataframe
                    st.write(f"Variables for Table ID: {entry}")
                    # sort dataframe by variable
                    df = df.sort_values(by='Variable')
                    st.dataframe(df)
                else:
                    st.write("No variables found for the selected Table ID.")
            else:
                st.error("Failed to fetch variables.")
    
    # Initialize session state for the button
    if 'load_map' not in st.session_state:
        st.session_state.load_map = False

    st.write("")
    st.write("")
    st.markdown(
        "<h5 style='text-align: center;'>Mapping Census Data</div>", 
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([3, 1])
    with col1:
        metric = st.text_input("Enter the metric variable ID to map (see census tables for more info)", "B19013_001E")
    with col2:
            # Button to load the map
        st.write("")
        st.write("")
        if st.toggle("Load map"):
            st.session_state.load_map = True

    

    if st.session_state.load_map:
        df = get_census_data(api_key, metric, year)
        df = df[df[metric] != -666666666]
        gdf = merge_with_shapefile(df)
        # st.dataframe(gdf)

        # Create a base Folium map
        m = folium.Map(location=[43.04041857049036, -76.14400626122578], zoom_start=12)  # Coordinates for Syracuse, NY

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
            fill_color='PuBuGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=metric
        ).add_to(m)

        # Add GeoDataFrame polygons to the map with custom styles
        folium.GeoJson(
            data=gdf,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(fields=['tract_number', metric], aliases=['Tract:', f'{metric}:'])
        ).add_to(m)

        # Add tract labels
        for _, row in gdf.iterrows():
            centroid = row['geometry'].centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(html=f"""<div style="font-size: 12px; color: black;">{row['tract_number']}</div>""")
            ).add_to(m)

        # Display the Folium map in Streamlit
        st.title(f"Map of {metric}")
        st_folium(m, width=700, height=500)


        with tempfile.TemporaryDirectory() as tmpdirname:
            shapefile_path = os.path.join(tmpdirname, "syracuse_census_data.shp")
            gdf.to_file(shapefile_path)
            
            zip_path = os.path.join(tmpdirname, "syracuse_census_data.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for ext in ['shp', 'shx', 'dbf', 'prj', 'cpg']:
                    file_path = shapefile_path.replace('.shp', f'.{ext}')
                    zipf.write(file_path, os.path.basename(file_path))
            
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="Download Shapefile",
                    data=f,
                    file_name=f"syracuse-{metric}-{year}.zip",
                    mime="application/zip"
                )

            

        
