import streamlit as st
from PIL import Image
import os
from RealEstateTracker import preprocessing
import webbrowser


st.set_page_config(
    page_title="Real Estate Tracker",
    page_icon="🗺",
    layout="wide",
    initial_sidebar_state="collapsed")

st.markdown( """ <style> .css-1siy2j7 {
    background-color: rgb(206 212 223);
}
</style> """, unsafe_allow_html=True, )

# With CSS add a background and set the font colors

CSS = """
h1 {
    color: white;
    text-align: letf;
    text-shadow: 0 0 3px #000000;}
h2 {color: white;
    text-align: left;
    text-shadow: 0 0 3px #000000;}
h3 {color: white;
    text-align: left;
    text-shadow: 0 0 3px #000000;}
p {color: white;
    text-align: left;
    text-shadow: 0 0 3px #000000;}


.stApp {
    background-image: linear-gradient(to bottom, rgba(153, 153, 153, 0.9), rgba(153, 153, 153, 0.9)), url(https://images.unsplash.com/photo-1516156008625-3a9d6067fab5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80);
    background-size: cover;}

.css-ocqkz7 {
    display: flex;
    flex-wrap: nowrap;
    -webkit-box-flex: 1;
    flex-grow: 1;
    -webkit-box-align: stretch;
    align-items: center;
    gap: 10rem;
    flex-direction: row;
    align-content: center;
    justify-content: center;
}

.css-1cpxqw2 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    margin: 0px;
    line-height: 2.6;
    color: #1d1d1e;
    width: inherit;
    user-select: none;
    background-color: rgb(170 230 225);
    border: 1px solid rgba(49, 51, 63, 0.2);
}

"""
# Import image/logo
image = Image.open(os.path.dirname(preprocessing.__file__)+'/data/Pray_for_Ukraine.png')
# Implement the CSS

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# Create columns in the layout

col1, col2 = st.columns(2)

# Title in the website

col1.write('''
# Real Estate Tracker
''')


# Description of the app


col1.write('''
### Unsure about what real estate listings are interesting market opportunities?


RealEstateTracker handles everything from the research to the market price prediction of a given asset for you. We do this using an in-house AI algorithm that we trained using real-time data from listing websites.

''')

if col1.button("Try it!"):
    webbrowser.open('http://localhost:8501/App', new = 2)

col2.image(image)
