import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Ensure you have latitude and longitude in your DataFrame
# You might have to modify this URL or your DataFrame to include these columns

# Dashboard Header and Layout
st.title('Countries Mentioned in US National Security Strategy Document')

# Use a slider for selecting the year
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_year = st.slider('Select a year:', min_value=min_year, max_value=max_year, value=min_year, step=1)

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Add a country filter with specific options
country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

# Filter data based on country selection
if country_option == 'Exclude United States':
    filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']
else:
    filtered_df = year_filtered_df

# Assuming 'Latitude' and 'Longitude' columns exist in your DataFrame
# Prepare data for the heatmap
heatmap_data = filtered_df.groupby(['Latitude', 'Longitude', 'Country']).sum().reset_index()

# Define a layer for the heatmap
layer = pdk.Layer(
    'HeatmapLayer',
    data=heatmap_data,
    opacity=0.9,
    get_position=['Longitude', 'Latitude'],
    get_weight='Count',
    radius_pixels=60
)

# Set the viewport location
view_state = pdk.ViewState(latitude=heatmap_data['Latitude'].mean(), longitude=heatmap_data['Longitude'].mean(), zoom=1)

# Render the deck.gl map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
