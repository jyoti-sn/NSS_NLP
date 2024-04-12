import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_country_updated.csv')

# Definitions of G-5 and G-20 countries
G5_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Japan']
G20_countries = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 
                 'India', 'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russian Federation', 'Saudi Arabia', 
                 'South Africa', 'Korea, Republic of', 'Turkey', 'United Kingdom', 'United States', 'European Union']

# Dashboard Header and Layout
st.title('Countries in the US National Security Strategy Document')

# Use a slider for selecting the year, limited to available years in the data
available_years = df['Year'].unique()
available_years.sort()
selected_year = st.slider('Select a year:', min_value=min(available_years), max_value=max(available_years), value=min(available_years))

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Country filter for excluding or including the United States
country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

# Apply US filter to the dataframe
if country_option == 'Exclude United States':
    year_filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']

# Group Selection for G-5 or G-20
group_option = st.radio("Select Group:", ('G-5', 'G-20'))

# Apply group filter
if group_option == 'G-5':
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries)]
else:
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G20_countries)]

# Calculate the total counts for the year and for each group
total_count_year = year_filtered_df['Count'].sum()
group_percentage = group_df.groupby('Country')['Count'].sum() / total_count_year * 100

# Display the heatmap and bar chart for all countries
heatmap_data = year_filtered_df.groupby(['Latitude', 'Longitude', 'Country']).sum().reset_index()
layer = pdk.Layer(
    'HeatmapLayer',
    data=heatmap_data,
    opacity=0.9,
    get_position=['Longitude', 'Latitude'],
    get_weight='Count',
    radius_pixels=60
)
view_state = pdk.ViewState(latitude=heatmap_data['Latitude'].mean(), longitude=heatmap_data['Longitude'].mean(), zoom=1)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

bar_chart_data = year_filtered_df.groupby('Country')['Count'].sum()
st.bar_chart(bar_chart_data)

# Display group specific data
st.header(f"{group_option} Countries' Mention Percentages")
st.bar_chart(group_percentage)

