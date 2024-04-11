import streamlit as st
import pandas as pd

# Load the data into a Pandas DataFrame (assuming you have a 'data.csv' file)
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Dashboard Header and Layout
st.title('Country Counts Dashboard')
selected_year = st.selectbox('Select a year:', df['Year'].unique())

# Filter data based on selected year
filtered_df = df[df['Year'] == selected_year]

# Choose your visualization library (here, using Plotly)
import plotly.express as px

fig = px.bar(filtered_df, x='Country', y='Count')

# Display the plot
st.plotly_chart(fig)
