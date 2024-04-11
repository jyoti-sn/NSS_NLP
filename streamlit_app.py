import streamlit as st
import pandas as pd

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Focus only on 'United States' entries
us_df = df[df['Country'] == 'United States']

# Dashboard Header and Layout
st.title('United States Mentions in US National Security Strategy Document')

# Use a slider for selecting the year
min_year = int(us_df['Year'].min())
max_year = int(us_df['Year'].max())
selected_year = st.slider('Select a year:', min_value=min_year, max_value=max_year, value=min_year, step=1)

# Filter data based on selected year
filtered_df = us_df[us_df['Year'] == selected_year]

# Display information about the selected year
if not filtered_df.empty:
    st.write(f'Mentions of the United States in {selected_year}: {filtered_df["Count"].iloc[0]}')
else:
    st.write("No mentions of the United States found for this year.")
