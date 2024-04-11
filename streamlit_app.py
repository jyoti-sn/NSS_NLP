pip install streamlit pandas plotly
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Country.csv')

# Dashboard Header and Layout
st.title('Countries Mentioned in US National Security Strategy Document')

# Using sidebar for input controls
st.sidebar.header("Input Options")
selected_year = st.sidebar.selectbox('Select a year:', df['Year'].unique())

# Filter data based on selected year
filtered_df = df[df['Year'] == selected_year]

# Plotting with Plotly for interactive charts
fig = px.bar(filtered_df, x='Country', y='Count', title=f"Countries Mentioned in {selected_year}",
             labels={"Count": "Mention Count"}, color='Country')
fig.update_layout(xaxis={'categoryorder':'total descending'})

# Display the interactive chart
st.plotly_chart(fig)

# Option to show the data table
if st.sidebar.checkbox('Show Data Table'):
    st.dataframe(filtered_df)
