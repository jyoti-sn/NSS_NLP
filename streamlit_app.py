import streamlit as st
import pandas as pd

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

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

# Use Streamlit's built-in bar chart to display the data
st.bar_chart(filtered_df.groupby('Country')['Count'].sum())
