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

# Use a multiselect box to allow users to select countries
selected_countries = st.multiselect('Select countries:', options=year_filtered_df['Country'].unique(), default=year_filtered_df['Country'].unique())

# Filter data further based on selected countries
filtered_df = year_filtered_df[year_filtered_df['Country'].isin(selected_countries)]

# Display the bar chart using Streamlit's built-in functionality
if not filtered_df.empty:
    st.bar_chart(filtered_df.groupby('Country')['Count'].sum())
else:
    st.write("No data to display.")

