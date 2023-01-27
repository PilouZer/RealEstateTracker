import streamlit as st
import pandas as pd
import numpy as np
import joblib
import webbrowser
from unidecode import unidecode

# Header configuration

st.set_page_config(
    page_title="Real Estate Tracker",
    page_icon="🗺",
    layout="centered",
    initial_sidebar_state="collapsed")


# With CSS add a background and set the font colors

CSS = """
h1 {
    color: white;
    text-align: center;
}

h2 {color: white;
    text-align: center;}
h3 {color: white;
    text-align: center;}
p {color: white;
    text-align: center;}


.stApp {
    background-image: linear-gradient(to bottom, rgba(153, 153, 153, 0.52), rgba(153, 153, 153, 0.52)), url(https://images.unsplash.com/photo-1516156008625-3a9d6067fab5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80);
    background-size: cover;

}
"""

# Implement the CSS

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# Title in the website

'''
# Real Estate Tracker
'''

# Description of the user options

'''
## Your dream house is waiting for you...

Enter your preference and look for opportunities
'''

# Neighborhood selection

'''## Select a neighborhood ##'''

df = ['Chamberí', 'Retiro', 'Carabanchel', 'Villa de Vallecas', 'Centro',
       'Tetuán', 'Puente de Vallecas', 'Barrio de Salamanca', 'Chamartín',
       'Usera', 'Moncloa - Aravaca', 'Ciudad Lineal', 'Arganzuela',
       'Fuencarral - El Pardo', 'Villaverde', 'Latina', 'Moratalaz',
       'Vicálvaro', 'Barajas', 'Hortaleza', 'Madrid Capital', 'San Blas']

neighborhood = st.selectbox('', df)

# Rooms selection

"""## Enter rooms number ##"""

pick_rooms = st.slider('', 0, 6, 1)

## Customize the slider bar

ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
    background: rgb(0 0 0 / 0%); } </style>''', unsafe_allow_html = True)


Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
    background-color: rgb(255, 250, 250); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)


Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                                { color: rgb(255, 250, 250); } </style>''', unsafe_allow_html = True)


col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
    background: linear-gradient(to right, rgb(255, 250, 250) 100%,
                                rgb(1, 183, 158) {pick_rooms}%,
                                rgba(151, 166, 195, 0.25) {pick_rooms}%,
                                rgba(151, 166, 195, 0.25) 100%); }} </style>'''

ColorSlider = st.markdown(col, unsafe_allow_html = True)


# Surface selection

"""## Enter the surface ##"""

surface = st.number_input("", min_value=20, max_value=None, value=50, step=1)


# Type of properties selection

'''## Select the type of property ##'''

df1 = ['Piso', 'Dúplex', 'Apartamento', 'Ático', 'Loft', 'Planta baja',
       'Finca rústica', 'Estudio', 'Casa adosada', 'Casa o chalet']

# Spanish-English dictionary of types

df1_eng = {'Piso':'Flat',
           'Dúplex':'Duplex',
           'Apartamento':'Apartment',
           'Ático':'Attic',
           'Loft':'Loft',
           'Planta baja':'Ground floor',
           'Finca rústica':'Rural property',
           'Estudio':'Study',
           'Casa adosada':'Single-family semi-detached',
           'Casa o chalet':'House or chalet'}

df1_trans = {"Flat": "Piso",
            "Duplex": "Dúplex",
            "Apartment": "Apartamento",
            "Attic": "Ático",
            "Loft": "Loft",
            "Ground floor": "Planta baja",
            "Rural property": "Finca rústica",
            "Study": "Estudio",
            "Single-family semi-detached": "Casa adosada",
            "House or chalet": "Casa o chalet"}

type = st.selectbox("", df1_eng.values())

"""
"""

# Creating columns in the layout

col1, col2, col3 , col4, col5 = st.columns(5)


param1 = {"pick_rooms": pick_rooms,
         "surface": surface,
         "neighborhood": neighborhood,
         'type': df1_trans[type]}

param = pd.DataFrame(param1, index=[0]).rename(columns={"pick_rooms":"rooms",
                                                "surface": "surface",
                                                "neighborhood": "neighborhood",
                                                "type": "nhousetype"})

# Importing model

potato = joblib.load("model.joblib")
pred = potato.predict(param)[0]

# Creating lower and upper bounds from price predition

price_low = "{:,}".format(int(pred * 0.95))
price_up = "{:,}".format(int(pred * 1.05))

final_pred = f"The market price for a {param1['type']} with {param1['surface']}m² in {param1['neighborhood']} is between {price_low}€ and {price_up}€"

# format the city string to fit in the url

city = ((unidecode(param1['neighborhood']).lower())).replace(' ', '-')

# create bins for surface m2

an_array = np.array([param1["surface"]])
bins = list(range(60,300,20))
bin_indices = np.digitize(an_array, bins)
sqr_meter = [60 + x*20 for x in bin_indices][0]

# Url with the specified features

if bin_indices[0] != 0:
    base_url = f"https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/{city}/l?maxPrice={int(pred * 0.95)}&maxSurface={sqr_meter}&minRooms={param1['pick_rooms']}&minSurface={sqr_meter - 20}"
else:
    base_url = f"https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/{city}/l?maxPrice={int(pred * 0.95)}&maxSurface={sqr_meter}&minRooms={param1['pick_rooms']}"


# Buttons for prediction and web redirection


if col2.button("Get the market price"):
    st.balloons()
    #st.write(final_pred)
    new_title = f'<p style="font-family:; color:White; font-size: 32px;">{final_pred}</p>'
    st.markdown(new_title, unsafe_allow_html=True)

if col4.button('Show me options!'):
    st.snow()
    webbrowser.open_new_tab(base_url)
