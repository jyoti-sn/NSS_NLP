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
st.title('Countries Mentioned in US National Security Strategy Document')

# Use a slider for selecting the year
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_year = st.slider('Select a year:', min_value=min_year, max_value=max_year, value=min_year, step=1)

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Filter data for G-5 and G-20 countries
G5_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries)]
G20_df = year_filtered_df[year_filtered_df['Country'].isin(G20_countries)]

# Calculate the total counts for the year
total_count_year = year_filtered_df['Count'].sum()

# Calculate percentages for G-5 and G-20 countries
G5_percentage = G5_df.groupby('Country')['Count'].sum() / total_count_year * 100
G20_percentage = G20_df.groupby('Country')['Count'].sum() / total_count_year * 100

# Display pie charts using Streamlit
st.header("G-5 Countries' Mention Percentages")
st.bar_chart(G5_percentage)

st.header("G-20 Countries' Mention Percentages")
st.bar_chart(G20_percentage)


