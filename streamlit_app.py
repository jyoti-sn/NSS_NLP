import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import numpy as np

# Load the data into Pandas DataFrames
df1 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_country_coded_Google.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Summary_Topics.csv')

# Merge the DataFrames on the 'Year' column
df = pd.merge(df1, df2, on='Year')

# Presidential DataFrame
presidents_df = pd.DataFrame({
    "Year": [1987, 1988, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2002, 2006, 2010, 2015, 2017, 2022],
    "President": [
        "Ronald Reagan", "Ronald Reagan", "George H. W. Bush", "George H. W. Bush", 
        "George H. W. Bush", "Bill Clinton", "Bill Clinton", "Bill Clinton", 
        "Bill Clinton", "Bill Clinton", "Bill Clinton", "Bill Clinton", "Bill Clinton", 
        "George W. Bush", "George W. Bush", "Barack Obama", "Barack Obama", 
        "Donald Trump", "Joe Biden"
    ],
    "Party": [
        "Republican", "Republican", "Republican", "Republican", "Republican", 
        "Democratic", "Democratic", "Democratic", "Democratic", "Democratic", 
        "Democratic", "Democratic", "Democratic", "Republican", "Republican", 
        "Democratic", "Democratic", "Republican", "Democratic"
    ]
})

# Dashboard Header and Layout
st.set_page_config(layout="wide", page_title="How does the white house see the world?")
st.title('How does the white house see the world?')
st.subheader("Analysis of the US National Security Strategy Document")

# Definitions of G-5 and G-20 countries
G5_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Japan']
G20_countries = [
    'Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany',
    'India', 'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russian Federation', 'Saudi Arabia',
    'South Africa', 'Korea, Republic of', 'Turkey', 'United Kingdom', 'United States', 'European Union'
]

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Apply US filter to the dataframe
if country_option == 'Exclude United States':
    year_filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']

# Apply group filter
if group_option == 'G-5':
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries)]
else:
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G20_countries)]


# Sidebar layout
with st.sidebar:
    # Use a slider for selecting the year
    selected_year = st.select_slider('Select a year:', options=presidents_df['Year'].unique())

    # Country filter for excluding or including the United States
    country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

    # Group Selection for G-5 or G-20
    group_option = st.radio("Select Group:", ('G-5', 'G-20'))


# Continent analysis
continent_data = year_filtered_df.groupby('Continent')['Count'].sum()
continent_percentage = (continent_data / year_filtered_df['Count'].sum()) * 100

# Display the bar chart for continents
st.header("Total Mentions by Continent")
col1, col2 = st.columns(2)
with col1:
    st.bar_chart(continent_data)
with col2:
    st.bar_chart(continent_percentage)

# Display Presidential Information
president_info = presidents_df[presidents_df['Year'] == selected_year]
if not president_info.empty:
    st.write(f"President in {selected_year}: {president_info['President'].values[0]} ({president_info['Party'].values[0]} Party)")

# Display the heatmap
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
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={
    "html": "<b>{Country}</b><br>Mentions: {Count}",
    "style": {"color": "white", "font-family": "Arial", "font-size": "12px", "padding": "10px"}
}))

