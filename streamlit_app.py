import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_country_updated.csv')

# Presidential DataFrame
presidents_df = pd.DataFrame({
    "Year": list(range(1987, 1989)) + list(range(1989, 1993)) + list(range(1993, 2001)) +
            list(range(2001, 2009)) + list(range(2009, 2017)) + list(range(2017, 2021)) + list(range(2021, 2025)),
    "President": ["Ronald Reagan"] * 2 + ["George H. W. Bush"] * 4 + ["Bill Clinton"] * 8 + ["George W. Bush"] * 8 +
                 ["Barack Obama"] * 8 + ["Donald Trump"] * 4 + ["Joe Biden"] * 4,
    "Party": ["Republican"] * 2 + ["Republican"] * 4 + ["Democratic"] * 8 + ["Republican"] * 8 +
             ["Democratic"] * 8 + ["Republican"] * 4 + ["Democratic"] * 4
})

# Definitions of G-5 and G-20 countries
G5_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Japan']
G20_countries = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany',
                 'India', 'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russian Federation', 'Saudi Arabia',
                 'South Africa', 'Korea, Republic of', 'Turkey', 'United Kingdom', 'United States', 'European Union']

# Dashboard Header and Layout
st.title('How does the White House see the world?')
st.subheader("Analysis of the US National Security Strategy Document")

# Use a slider for selecting the year
available_years = df['Year'].unique()
available_years.sort()
col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.slider('Select a year:', min_value=min(available_years), max_value=max(available_years), value=min(available_years))

# Display Presidential Information
president_info = presidents_df[presidents_df['Year'] == selected_year]
if not president_info.empty:
    with col2:
        st.write(f"President in {selected_year}: {president_info['President'].values[0]}")
    with col3:
        st.write(f"Party: {president_info['Party'].values[0]}")

# Country filter for excluding or including the United States
with col1:
    country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

# Apply US filter to the dataframe
if country_option == 'Exclude United States':
    year_filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']

# Group Selection for G-5 or G-20
with col2:
    group_option = st.radio("Select Group:", ('G-5', 'G-20'))

# Apply group filter
if group_option == 'G-5':
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries)]
else:
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G20_countries)]

# Calculate the total counts for the year and for each group
total_count_year = year_filtered_df['Count'].sum()
group_percentage = group_df.groupby('Country')['Count'].sum() / total_count_year * 100

# Display the heatmap
st.pydeck_chart(pdk.Deck(
    layers=[pdk.Layer(
        'HeatmapLayer', data=year_filtered_df.groupby(['Latitude', 'Longitude', 'Country']).sum().reset_index(),
        opacity=0.9, get_position=['Longitude', 'Latitude'], get_weight='Count', radius_pixels=60)],
    initial_view_state=pdk.ViewState(latitude=year_filtered_df['Latitude'].mean(), longitude=year_filtered_df['Longitude'].mean(), zoom=1)
))

# Display bar charts side by side for counts and percentages
col4, col5 = st.columns(2)
with col4:
    st.header("Total Mentions by Country")
    st.bar_chart(year_filtered_df.groupby('Country')['Count'].sum())

with col5:
    st.header(f"{group_option} Countries' Mention Percentages")
    st.bar_chart(group_percentage)


