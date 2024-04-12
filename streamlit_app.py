import streamlit as st
import pandas as pd
import pydeck as pdk
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Load the data into Pandas DataFrames
df1 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_country_updated.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Summary_Topics.csv')

# Merge the DataFrames on the 'Year' column
df = pd.merge(df1, df2, on='Year')

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
st.subheader("Analysis of the US National Security Strategy Document")

# Use a slider for selecting the year
available_years = df['Year'].unique()
available_years.sort()
selected_year = st.sidebar.slider('Select a year:', min_value=min(available_years), max_value=max(available_years), value=min(available_years))

# Filter data based on selected year
year_filtered_df = df[df['Year'] == selected_year]

# Display Presidential Information
president_info = presidents_df[presidents_df['Year'] == selected_year]
if not president_info.empty:
    st.write(f"President in {selected_year}: {president_info['President'].values[0]} ({president_info['Party'].values[0]} Party)")

# Country filter for excluding or including the United States
country_option = st.sidebar.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

# Apply US filter to the dataframe
if country_option == 'Exclude United States':
    year_filtered_df = year_filtered_df[year_filtered_df['Country'] != 'United States']

# Group Selection for G-5 or G-20
group_option = st.sidebar.radio("Select Group:", ('G-5', 'G-20'))

# Apply group filter
if group_option == 'G-5':
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G5_countries)]
else:
    group_df = year_filtered_df[year_filtered_df['Country'].isin(G20_countries)]

# Calculate the total counts for the year and for each group
total_count_year = year_filtered_df['Count'].sum()
group_percentage = group_df.groupby('Country')['Count'].sum() / total_count_year * 100

# Display the heatmap and bar chart for all countries
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

# Display the heatmap and bar chart
col1, col2 = st.columns(2)
with col1:
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={
        "html": "<b>{Country}</b><br>Mentions: {Count}",
        "style": {"color": "white", "font-family": "Arial", "font-size": "12px", "padding": "10px"}
    }))

with col2:
    st.header("Total Mentions by Country")
    bar_chart_data = year_filtered_df.groupby('Country')['Count'].sum()
    st.bar_chart(bar_chart_data, use_container_width=True)
    st.write(f"Total mentions in {selected_year}: {int(total_count_year)}")

# Display group specific data
st.header(f"{group_option} Countries' Mention Percentages")
group_percentage_chart = st.bar_chart(group_percentage, use_container_width=True)
st.write(f"Total mentions for {group_option} countries in {selected_year}: {int(group_df['Count'].sum())}")

# Create a word cloud based on the 'Summary Topics' for the selected year
st.header("Top topics mentioned in this year")
summary_topics = year_filtered_df['Summary_Topics'].str.split(',').explode().value_counts()
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=400).generate_from_frequencies(summary_topics)
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)
