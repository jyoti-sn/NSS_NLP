import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to fetch latitude and longitude
def get_lat_lon(country):
    try:
        location = geolocator.geocode(country)
        return location.latitude, location.longitude
    except:
        return None, None

# Apply function to get coordinates
df['lat'], df['lon'] = zip(*df['Country'].apply(get_lat_lon))

# Dashboard Header
st.title('Heatmap of Countries Mentioned in US National Security Strategy Document')

# Year slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_year = st.slider('Select a year:', min_value=min_year, max_value=max_year, value=min_year, step=1)

# Filter data based on the selected year
year_filtered_df = df[df['Year'] == selected_year]

# Create a heatmap layer
layer = pdk.Layer(
    "HeatmapLayer",
    data=year_filtered_df,
    opacity=0.9,
    get_position=["lon", "lat"],
    aggregation='"SUM"',
    get_weight="Count",
    threshold=1,
    get_radius=100000,  # Radius is in meters
)

# Set the viewport location
view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1, bearing=0, pitch=0)

# Render the deck.gl map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

# Display the map
st.pydeck_chart(r)
