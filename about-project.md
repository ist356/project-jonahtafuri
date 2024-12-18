# About My Project

Student Name:  Jonah Tafuri
Student Email:  jttafuri@syr.edu

### What it does
My project utilizes the Census API dataset with the Streamlit UI to allow users to load a variable of their choice from any of the American Community Surveys (ACS) onto a map of Syracuse and download a geopandas dataframe as a shapefile upon completion. The program allows users to view the choices of census tables as well as all of the variables within any given table.

### How you run my project
Run census_call to load the functions in the script (I am not completely sure this step is necessary). Run streamlit for streamlit_ui (DO NOT USE THE OLD ONE) and enter a census API key (I emailed one to Professor Fudge). Then from there you can select the census year. Based on the dataframe of Census tables within the selected they can enter any table's name to view the variables associated with the table. Finally they can enter the measurement they wish to see mapped and a choropleth map of the census variable they requested will be generated over Syracuse. They can then download the dataframe as a shapefile if they wish.