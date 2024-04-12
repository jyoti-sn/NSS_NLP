import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the data into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_country_updated.csv')

# Presidential DataFrame
presidents_df = pd.DataFrame({
    "Year": sum([list(range(start, end)) for start, end in 
        zip([1987, 1989, 1993, 2001, 2009, 2017, 2021], [1989, 1993, 2001, 2009, 2017, 2021, 2025])], []),
    "President": ["Ronald Reagan"] * 2 + ["George H. W. Bush"] * 4 + ["Bill Clinton"] * 8 +
                 ["George W. Bush"] * 8 + ["Barack Obama"] * 8 + ["Donald Trump"] * 4 + ["Joe Biden"] * 4,
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
selected_year = st.slider('Select a year:', min_value=min(available_years), max_value=max(available_years), value=min(available_years))

# Display Presidential Information
president_info = presidents_df[presidents_df['Year'] == selected_year]
if not president_info.empty:
    st.write(f"President in {selected_year}: {president_info['President'].values[0]} ({president_info['Party'].values[0]} Party)")

# Country filter for excluding or including the United States
country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Apply US filter to the dataframe
if country_option == 'Exclude United States':
    year_filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']

# Group Selection for G-5 or G-20
group_option = st.radio("Select Group:", ('G-5', 'G-20'))

# Apply group filter
group_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries if group_option == 'G-5' else G20_countries)]

# Calculate the total counts for the year and for each group
total_count_year = year_filtered_df['Count'].sum()
group_percentage = group_df.groupby('Country')['Count'].sum() / total_count_year * 100

# Display the heatmap
heatmap_data = year_filtered_df.groupby(['Latitude', 'Longitude', 'Country']).sum().reset_index()
layer = pdk.Layer(
    'HeatmapLayer', data=heatmap_data, opacity=0.9,
    get_position=['Longitude', 'Latitude'], get_weight='Count', radius_pixels=60
)
view_state = pdk.ViewState(latitude=heatmap_data['Latitude'].mean(), longitude=heatmap_data['Longitude'].mean(), zoom=1)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Bar chart for all country counts
st.header("Total Mentions by Country")
st.bar_chart(year_filtered_df.groupby('Country')['Count'].sum())

# Display group specific data
st.header(f"{group_option} Countries' Mention Percentages")
st.bar_chart(group_percentage)


