import streamlit as st
import pandas as pd
import pydeck as pdk
import re

# Load the data into Pandas DataFrames
df1 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_country_coded_Google.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/US_NSS_Full_Texts.csv')

# Convert 'Year' column in df2 to datetime and then to year data type
df2['Year'] = pd.to_datetime(df2['Year'], format='%Y').dt.year

# Merge the DataFrames on the 'Year' column
df = pd.merge(df1, df2, on='Year')

# Convert 'Text' column to lowercase
df['Text'] = df['Text'].str.lower()

# Presidential DataFrame
presidents_df = pd.DataFrame({
    "Year": list(range(1987, 1989)) + list(range(1989, 1993)) + list(range(1993, 2001)) + list(range(2001, 2009)) +
            list(range(2009, 2017)) + list(range(2017, 2021)) + list(range(2021, 2025)),
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
st.set_page_config(layout="wide", page_title="How does the white house see the world?")
st.title('How does the white house see the world?')
st.subheader("Analysis of the US National Security Strategy Document: 1987-2022")

# Sidebar layout
with st.sidebar:
    # Use a slider for selecting the year
    available_years = [1987, 1988, 1990, 1991, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2002, 2006, 2010, 2015, 2017, 2022]
    selected_year = st.slider('Select a year:', min_value=min(available_years), max_value=max(available_years), value=min(available_years))

    # Country filter for excluding or including the United States
    country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

    # Group Selection for G-5 or G-20
    group_option = st.radio("Select Group:", ('G-5', 'G-20'))

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Display Presidential Information
president_info = presidents_df[presidents_df['Year'] == selected_year]
if not president_info.empty:
    st.write(f"President in {selected_year}: {president_info['President'].values[0]} ({president_info['Party'].values[0]} Party)")

# Apply US filter to the dataframe
if country_option == 'Exclude United States':
    year_filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']

# Apply group filter
if group_option == 'G-5':
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries)]
else:
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G20_countries)]

# Calculate the total counts for the year and for each group
total_count_year = year_filtered_df['Count'].sum()
group_percentage = group_df.groupby('Country')['Count'].sum() / total_count_year * 100

# Display the heatmap
heatmap_data = year_filtered_df.groupby(['Latitude', 'Longitude', 'Country']).sum().reset_index()
layer = pdk.Layer(
    'HeatmapLayer',
    data=heatmap_data,
    opacity=0.9,
    get_position=['Longitude', 'Latitude'],
    get_weight='Count',
    radius_pixels=60
)
view_state = pdk.ViewState(latitude=heatmap_data['Latitude'].mean(), longitude=heatmap_data['Longitude'].mean(), zoom=1)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={
    "html": "<b>{Country}</b><br>Mentions: {Count}",
    "style": {"color": "white", "font-family": "Arial", "font-size": "12px", "padding": "10px"}
}))

# Display the bar charts
col1, col2 = st.columns(2)
with col1:
    st.header("Total Mentions by Country")
    bar_chart_data = year_filtered_df.groupby('Country')['Count'].sum()
    st.bar_chart(bar_chart_data, use_container_width=True)
    st.write(f"Total mentions in {selected_year}: {int(total_count_year)}")

with col2:
    st.header(f"{group_option} Countries' Mention Percentages")
    group_percentage_chart = st.bar_chart(group_percentage, use_container_width=True)
    st.write(f"Total mentions for {group_option} countries in {selected_year}: {int(group_df['Count'].sum())}")

# Create a bar chart for Continents
st.header("Total Mentions by Continent")
continent_mentions = year_filtered_df.groupby('Continent')['Count'].sum()
continent_percentage = continent_mentions / total_count_year * 100

col3, col4 = st.columns(2)
with col3:
    st.subheader("Total Mentions")
    st.bar_chart(continent_mentions, use_container_width=True)

with col4:
    st.subheader("Mention Percentage")
    st.bar_chart(continent_percentage, use_container_width=True)

# Word search over time
st.subheader("Word Frequency Over Time")
search_word = st.text_input("Enter a word to search:").lower()
if search_word:
    word_counts = df[df['Text'].str.contains(search_word, case=False)].groupby('Year')['Text'].count().reset_index()
    st.line_chart(data=word_counts, x='Year', y='Text')
    st.write(f"Normalised frequency of the word '{search_word}' in the NSS documents over the years.")

    # Calculate correlation with party (normalized)
    merged_df = pd.merge(df, presidents_df, on='Year')
    republican_years = merged_df['Party'].value_counts()['Republican']
    democratic_years = merged_df['Party'].value_counts()['Democratic']

    republican_mentions = merged_df[merged_df['Party'] == 'Republican']['Text'].str.contains(search_word).sum() / republican_years
    democratic_mentions = merged_df[merged_df['Party'] == 'Democratic']['Text'].str.contains(search_word).sum() / democratic_years

    total_mentions = republican_mentions + democratic_mentions

    if total_mentions > 0:
        republican_percentage = (republican_mentions / total_mentions) * 100
        democratic_percentage = (democratic_mentions / total_mentions) * 100

        # Display likelihood in large, bold font
        st.markdown(f"<div style='font-size: 24px; font-weight: bold;'>Republican: {republican_percentage:.1f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 24px; font-weight: bold;'>Democratic: {democratic_percentage:.1f}%</div>", unsafe_allow_html=True)
    else:
        st.write("The word was not found in the dataset.")
