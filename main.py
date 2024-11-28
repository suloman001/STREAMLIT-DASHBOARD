# IMPORTING LIBRARIES
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import plotly.express as px
from folium.plugins import Geocoder, MiniMap,Fullscreen,Draw






# GETTING THE PATH TO THE WORLD DATA
path_of_the_world_data = "world_population (1).csv"
path_of_json_world_data = "world.geojson"


# READING THE WORLD DATA
data = pd.read_csv(path_of_the_world_data)
geo_data = gpd.read_file(path_of_json_world_data)


# GETTING ACCESS TO STREAMLIT PAGE WITH A TITLE
st.set_page_config(page_title="WORLD POPULATION DASHBOARD", layout="wide")


# GIVEN A TITLE TO MY DASHBOARD
st.title("WORLD POPULATION DASHBOARD CREATED BY Sulaiman")
st.write("## Select a country to view its population data and geographical information")


# SELECTING A COUNTRY COLUMN BY ADDING AN EMPTY SPACE AT THE FIRST PLACE
country = [""] + list(data["Country/Territory"].unique())
select_a_country = st.selectbox("Select A Country Of Your Choice", country)


# CREATING COLUMNS FOR SIDE BY SIDE LAYOUT
col1, col2 = st.columns(2)


# WHAT TO DISLAY AT COLUMN ONE 
with col2:
    if select_a_country:
        #  EXTRACTING POPULATION DATA FOR THE SELECTED COUNTRY
        country_data = data[data["Country/Territory"] == select_a_country].squeeze()
        
        # DISPLAYING POPULATION RELATED INFORMATIONS
        st.write(f"### STATISTICS OF {select_a_country} ")# the (###)sign over here  will make it Bold 
        country_info = country_data[["Area (km²)", "Density (per km²)", "World Population Percentage", "Growth Rate"]].to_frame().T

        #DISPLAYING THE COUNTRY INFORMATION IN TABLE FORM
        st.table(country_info)



 #WHAT TO DISPLAY AT COLUMN ONE       
with col1:
        # VARIOUS YEARS NEEDED FOR VISUALISATION
        years=["1970 Population", "1980 Population", "1990 Population", "2000 Population", "2010 Population", "2015 Population", "2020 Population", "2022 Population"]
       

        #ENABLING THE USER CHOOSE THE VARIOUS YEARS NEEDED FOR VISUALISATION
        years_select = st.multiselect("Select The Years You Want To Visualize Their Populations", options=years)

        # EXTRACTING THE SELECTED POPULATION DATA ACCORDING TO THE VARIOUS YEARS
        if years_select:
            population = country_data[["1970 Population", "1980 Population", "1990 Population", "2000 Population", "2010 Population", "2015 Population", "2020 Population", "2022 Population"]].values.tolist()
            selected_population = [population[years.index(year)] for year in years_select]
            
            data_pop = {
                "year": years_select,
                "populations": selected_population
            }
            df_population = pd.DataFrame(data_pop)

            # BAR PLOT FOR POPULATION VASUALISATION OF THE VARIOUS YEARS SELECTED
            fig = px.bar(
                df_population,
                x="year",
                y="populations",
                labels={"year": "Year", "populations": "Population"},
                text_auto=True,
                title=f"Population of {select_a_country} Over Selected Years"
            )

            #UPDATING FIGURE TO ENSURE THAT THE TITLE IS BIG ENOUGH IN THE GOOD FORMAT
            fig.update_layout(
                title=f"Population of {select_a_country} Over Selected Years",
                title_font=dict(family="Arial", size=24, color="white", weight="bold")
            )

            # SHOWING THE BAR PLOT
            st.plotly_chart(fig,height=1000)



# WHAT TO DISPLAY IN COLUMN TWO
with col2:
    if select_a_country:
        # FILTERING THE GEO_DATA  FOR THE SELECTED COUNTRY OF CHOICE
        filtered_geo_data = geo_data[geo_data["name"] == select_a_country]

        #DECISION TO MAKE IF THE GEO_DATA IS NOT EMPTY
        if not filtered_geo_data.empty:

            #GETTING THE CENTROID FOR THE MAP CENTERING
            filtered_geo_data = filtered_geo_data.to_crs(epsg=3857)  # Converting to Mercator CRS for accurate measurement
            centroid = filtered_geo_data.geometry.centroid.to_crs(epsg=4326).iloc[0]

            # CREATING A MAP CENTERED ON THE COUNTRY
            map = folium.Map(location=[centroid.y, centroid.x], zoom_start=5)
            folium.GeoJson(filtered_geo_data.to_crs(epsg=4326)).add_to(map)

            # ADDING A MARKER FOR THE CAPITAL CITY
            folium.Marker(
                location=[centroid.y, centroid.x],
                popup=f"Capital: {country_data['Capital']}",
                icon=folium.Icon(color="green", icon="cloud"),
            ).add_to(map)
            Geocoder().add_to(map)
            Fullscreen().add_to(map)
            Draw(export=True).add_to(map)
            MiniMap(position="bottomright").add_to(map)
            
            st.write(f"### Map Of {select_a_country}") 
            # DISPLAYING THE MAP IN A STREAMLIT
            st_folium(map, width=700, height=440)


        else:
            st.write("### No GeoJSON data found for the selected country!")


        

        
        
     





        

    