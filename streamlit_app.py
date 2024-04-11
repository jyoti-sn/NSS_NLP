{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMIfAm7pj4er4dRjX8g3vtO"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "RqNDpi677GET"
      },
      "outputs": [],
      "source": [
        "!pip install streamlit\n",
        "import streamlit as st\n",
        "# Choose your visualization library (here, using Plotly)\n",
        "import plotly.express as px\n",
        "import pandas as pd"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "df = read_csv('https://github.com/jyoti-sn/NSS_NLP/blob/main/NSS_Country.csv')"
      ],
      "metadata": {
        "id": "7PcN3SSI7Lim"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "st.title('Country Counts Dashboard')\n",
        "\n",
        "# Selectbox for year selection\n",
        "selected_year = st.selectbox('Select a year:', df['Year'].unique())\n",
        "\n",
        "# Filter data based on selected year\n",
        "filtered_df = df[df['Year'] == selected_year]\n",
        "\n",
        "fig = px.bar(filtered_df, x='Country', y='Count')\n",
        "\n",
        "# Display the plot\n",
        "st.plotly_chart(fig)"
      ],
      "metadata": {
        "id": "DBcljg9T7K9l"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}