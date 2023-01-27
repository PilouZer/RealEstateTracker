import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
import plotly.express as px
from RealEstateTracker.preprocessing import preprocess
from RealEstateTracker import preprocessing
import os


df = preprocess()

df_eng = {'Piso':'Flat',
           'Dúplex':'Duplex',
           'Apartamento':'Apartment',
           'Ático':'Attic',
           'Loft':'Loft',
           'Planta baja':'Ground floor',
           'Finca rústica':'Rural property',
           'Estudio':'Study',
           'Casa adosada':'Single-family semi-detached',
           'Casa o chalet':'House or chalet'}
df["nhousetype"] = df["nhousetype"].map(df_eng)

st.set_page_config(page_title="Real Estate Dashboard",

page_icon=":bar_chart:",

layout = "wide",

initial_sidebar_state="collapsed"
)

st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
                # .sidebar .sidebar-content {
                # background-image: linear-gradient(#2e7bcf,#2e7bcf);
                # color: white;
                # }
                .st-c7 {background-color: rgb(133 173 227);}
                .st-du {background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 0%, rgb(67 102 204) 0%, rgb(49 71 166) 16.6667%, rgba(151, 166, 195, 0.25) 16.6667%, rgba(151, 166, 195, 0.25) 100%);}
                .css-demzbm {background-color: rgb(133 173 227);}
        </style>
        """, unsafe_allow_html=True)

CSS = """
h1 {
    color: white;
    text-align: center;
    text-shadow: 0 0 2px #000000;
}

h2 {color: black;
    }
h3 {color: white;
    text-align: center;
    text-shadow: 0 0 2px #000000;
    }
p {color: white;
    text-align: center;
    text-shadow: 0 0 2px #000000;
    }


.stApp {
    background-image: linear-gradient(to bottom, rgba(153, 153, 153, 0.52), rgba(153, 153, 153, 0.52)), url(https://images.unsplash.com/photo-1516156008625-3a9d6067fab5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80);
    background-size: cover;

}

.user-select-none svg-container {
    border-radius: 43px;
    }


"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


#SIDEBAR
st.sidebar.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

st.sidebar.header("Please Filter Here:")

neighborhood = st.sidebar.multiselect("Select the neighborhood:",

options = df["neighborhood"].unique(),

# default = df["neighborhood"].unique(),

)



st.sidebar.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

nhousetype = st.sidebar.multiselect("Select the type of property:",

options=df["nhousetype"].unique(),

# default=df["nhousetype"].unique(),

)

min_room, max_room = st.sidebar.select_slider("Select the number of rooms:",

# options=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 18.0]
options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 18],
 value=(1, 3)

)

df_selection = df.query(f"neighborhood == @neighborhood & nhousetype == @nhousetype & rooms>={min_room} & rooms<={max_room}"

#"neighborhood == @neighborhood & nhousetype == @nhousetype & @min_room >= rooms & rooms <= @max_room "

)

# st.dataframe(df_selection)

# ---MAINPAGE ---


st.title("Real Estate Dashboard")


st.markdown("##")

# MAP


with open(os.path.dirname(preprocessing.__file__)+'/data/madrid-districts.geojson.json') as response:
    counties = json.load(response)

df["price_per_m2"] = (df["price"]/df["surface"]).astype(int)
data = df.groupby("neighborhood").price_per_m2.mean().astype(int).reset_index()

geojson = counties

fig = px.choropleth_mapbox(data, geojson=geojson, color="price_per_m2",
                           locations="neighborhood", featureidkey="properties.name",
                           center={"lat": 40.4167, "lon": -3.70325},
                           labels={'neighborhood':'Neighborhood'},
                           color_continuous_scale="Viridis",
                           opacity=0.6,
                           mapbox_style="carto-positron", zoom=9)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)


# TOP KPI's

average_price = int(df_selection["price"].mean()) if len(df_selection) > 0 else 0
average_m2 = int(df_selection["surface"].mean()) if len(df_selection) > 0 else 0
price_per_m2 = int((df_selection["price"]/df_selection["surface"]).mean()) if len(df_selection) > 0 else 0

# average_price = int(df_selection["price"].mean())

# average_m2 = int(df_selection["surface"].mean())

left_column, middle_column, right_column = st.columns(3)

with left_column:

    st.subheader("Price per m2:")

    st.subheader(f"EUR {price_per_m2:,}")

with middle_column:

    st.subheader("Average price:")

    st.subheader(f"EUR {average_price:,}")

with right_column:

    st.subheader("Average surface:")

    st.subheader(f"{average_m2:,} m2")

    st.markdown("---")
