import streamlit as st
import pandas as pd
import pydeck as pdk
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

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

# Sidebar layout
with st.sidebar:
    # Use a slider for selecting the year
    available_years = df['Year'].unique()
    available_years.sort()
    selected_year = st.slider('Select a year:', min_value=min(available_years), max_value=max(available_years), value=min(available_years))

    # Country filter for excluding or including the United States
    country_option = st.selectbox('Filter countries:', ['All Countries', 'Exclude United States'])

    # Group Selection for G-5 or G-20
    group_option = st.radio("Select Group:", ('G-5', 'G-20'))

    # Country correlation analysis
    st.subheader("Country Correlation Analysis")
    country1 = st.selectbox("Select Country 1", df['Country'].unique())
    country2 = st.selectbox("Select Country 2", df['Country'].unique())

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

# Create a word cloud based on the individual words in 'Summary Topics' for the selected year
st.header("Top topics mentioned in this year")
words_to_remove = ['united states', 'united states of america', 'national security strategy', 'national', 'security', 'strategy', 'america', 'american']
summary_topics = ' '.join(year_filtered_df['Summary_Topics'].str.split(',').explode())
summary_topics = ' '.join([word for word in summary_topics.split() if word.lower() not in words_to_remove])
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=400).generate(summary_topics)
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Country correlation analysis
import streamlit as st
import pandas as pd
import pydeck as pdk
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Load the data into Pandas DataFrames
df1 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_country_updated.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/jyoti-sn/NSS_NLP/main/NSS_Summary_Topics.csv')

# Merge the DataFrames on the 'Year' column
df = pd.merge(df1, df2, on='Year')

# Country correlation analysis
with st.sidebar:
    if country1 != country2:
        country1_data = df[df['Country'] == country1]['Count']
        country2_data = df[df['Country'] == country2]['Count']

        # Ensure both countries have data across all years
        if country1_data.size == country2_data.size:
            corr, p_value = stats.pearsonr(country1_data, country2_data)

            if abs(corr) >= 0.7:
                corr_description = "Very strong correlation"
            elif abs(corr) >= 0.5:
                corr_description = "Strong correlation"
            elif abs(corr) >= 0.3:
                corr_description = "Moderate correlation"
            else:
                corr_description = "Weak or no correlation"

            st.write(f"The correlation between {country1} and {country2} is {corr_description} with a correlation coefficient of {corr:.2f} and a p-value of {p_value:.2f}.")
        else:
            st.write(f"Correlation cannot be calculated: {country1} and {country2} might not have data for the same years.")
    else:
        st.write("Please select two different countries to perform the correlation analysis.")

# Word frequency line chart
with st.sidebar:
    st.subheader("Word Frequency Over Time")
    search_word = st.text_input("Enter a word to search:")
    if search_word:
        word_counts = df[df['Summary_Topics'].str.contains(search_word, case=False)].groupby('Year').size()
        st.line_chart(word_counts)

        st.write(f"The frequency of the word '{search_word}' in the 'Summary Topics' column over the years.")
