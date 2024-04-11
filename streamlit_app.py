import streamlit as st
import pandas as pd

# Load the data into a Pandas DataFrame (assuming you have a 'data.csv' file)
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Dashboard Header and Layout
st.title('Countries Mentioned in US National Security Strategy Document')
selected_year = st.selectbox('Select a year:', df['Year'].unique())

# Filter data based on selected year
filtered_df = df[df['Year'] == selected_year]

# Display the bar chart
st.bar_chart(filtered_df, x='Country', y='Count')
