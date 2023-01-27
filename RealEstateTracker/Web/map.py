import json
import plotly.express as px
import pandas as pd
import numpy as np
from RealEstateTracker import preprocessing

data = preprocessing.preprocess()

with open('../raw_data/madrid-districts.geojson.json') as response:
    counties = json.load(response)

df = data.groupby("neighborhood").price.mean().reset_index()
geojson = counties

fig = px.choropleth_mapbox(df, geojson=geojson, color="price",
                           locations="neighborhood", featureidkey="properties.name",
                           center={"lat": 40.4167, "lon": -3.70325},
                           labels={'neighborhood':'Neighborhood'},
                           color_continuous_scale="Viridis",
                           opacity=0.4,
                           mapbox_style="carto-positron", zoom=9.5)
fig.show()
