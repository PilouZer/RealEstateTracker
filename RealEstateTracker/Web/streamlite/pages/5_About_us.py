#from tkinter import CENTER
import streamlit as st
from PIL import Image
import os
from RealEstateTracker import preprocessing, utils

st.set_page_config(
    page_title="About Us",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed")

# padding_top = 0
# padding_bottom = 10
# padding_left = 1
# padding_right = 10
# # max_width_str = f'max-width: 100%;'

# st.markdown(f'''
#             <style>
#                 .reportview-container .sidebar-content {{
#                     padding-top: {padding_top}rem;
#                 }}
#                 .reportview-container .main .block-container {{
#                     padding-top: {padding_top}rem;
#                     padding-right: {padding_right}rem;
#                     padding-left: {padding_left}rem;
#                     padding-bottom: {padding_bottom}rem;
#                 }}
#             </style>
#             ''', unsafe_allow_html=True,
# )



st.markdown("""
        <style>
               .css-12oz5g7 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 2rem;
                    padding-right: 2rem;
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
    text-shadow: 0 0 3px #000000;
}

h2 {color: white;
    text-align: center;
    text-shadow: 0 0 3px #000000;}
h3 {color: white;
    text-align: center;
    text-shadow: 0 0 3px #000000;}
p {color: white;
    text-align: center;
    text-shadow: 0 0 3px #000000;
    }


.stApp {
    background-image: linear-gradient(to bottom, rgba(153, 153, 153, 0.9), rgba(153, 153, 153, 0.9)), url(https://images.unsplash.com/photo-1516156008625-3a9d6067fab5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80);
    background-size: cover;

}
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

st.title("About Us")
# st.sidebar.markdown("# Dashboard")


image = Image.open(os.path.dirname(preprocessing.__file__)+'/data/group.jpg')

st.image(image)

left_column, middle_column, right_column = st.columns(3)

linicon = Image.open(os.path.dirname(preprocessing.__file__)+'/data/linicon.png')
image_path = os.path.dirname(preprocessing.__file__)+'/data/linicon.png'
image_link_dan = "https://www.linkedin.com/in/daniel-sánchez-gómez-465760134"
image_link_luk = "https://www.linkedin.com/in/lucas-lenci-vinao/"
image_link_pie = "https://www.linkedin.com/in/pierre-louisberlemont/"

with left_column:

    st.subheader("Pierre-Louis Berlemont")
    # st.image(linicon, width=40)
    st.write(f'<a href="{image_link_pie}">{utils.image_tag(image_path)}</a>', unsafe_allow_html=True)

    # st.markdown("[![Foo](https://cdn-icons-png.flaticon.com/512/174/174857.png)](https://www.linkedin.com/in/daniel-sánchez-gómez-465760134)")
    st.write("BBA graduate pursuing a Master’s degree in Data Science. Through my work as a Business Analyst for a major European retailer, I realised how data is crucial for success in any company/industry. My objective at Le Wagon is to deep dive into Data Science in order to gain valuable technical skills and develop useful tools.")

with middle_column:

    st.subheader("Lucas Lenci Guerra")
    st.write(f'<a href="{image_link_luk}">{utils.image_tag(image_path)}</a>', unsafe_allow_html=True)
    st.write("Passionate about Data. I sell Bibles on my spare time")

with right_column:

    st.subheader("Daniel Sánchez Gómez")
    st.write(f'<a href="{image_link_dan}">{utils.image_tag(image_path)}</a>', unsafe_allow_html=True)
    st.write("English graduate with an MBA. After working in various roles in the localization industry, I wanted a change. I’ve always been interested in data, and after some consideration, I decided that my future was in data science, thus I joined Le Wagon.")
