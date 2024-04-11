import streamlit as st
# Choose your visualization library (here, using Plotly)
import pandas as pd
import plotly.express as px


df = read_csv('https://github.com/jyoti-sn/NSS_NLP/blob/main/NSS_Country.csv')

st.title('Country Counts Dashboard')

# Selectbox for year selection
selected_year = st.selectbox('Select a year:', df['Year'].unique())

# Filter data based on selected year
filtered_df = df[df['Year'] == selected_year]

fig = px.bar(filtered_df, x='Country', y='Count')

# Display the plot
st.plotly_chart(fig)
