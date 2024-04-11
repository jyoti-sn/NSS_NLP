import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Assuming we add latitude and longitude to the DataFrame
# This is a placeholder. You should replace it with actual latitude and longitude data.
# Example: df = df.merge(country_coords, on='Country', how='left')
df['lat'] = [random.uniform(-90, 90) for _ in range(len(df))]
df['lon'] = [random.uniform(-180, 180) for _ in range(len(df))]

# Dashboard Header
st.title('Heatmap of Countries Mentioned in US National Security Strategy Document')

# Year slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_year = st.slider('Select a year:', min_value=min_year, max_value=max_year, value=min_year, step=1)

# Filter data based on the selected year
year_filtered_df = df[df['Year'] == selected_year]

# Heatmap Layer
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

