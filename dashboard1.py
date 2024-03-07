import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    data_df = pd.read_csv("https://raw.githubusercontent.com/Danendracleo/Guanyuan.csv/main/PRSA_Data_Guanyuan_20130301-20170228.csv")
    return data_df

data_df = load_data()

# Sidebar
analysis_type = st.sidebar.selectbox("Select Analysis Type:", ["Mean over 5 Years", "Individual Year"])

if analysis_type == "Individual Year":
    selected_year = st.sidebar.selectbox("Select Year:", data_df["year"].unique())
    selected_year_data = data_df[data_df["year"] == selected_year]

# JUDUL STREAMLIT
st.title("Guanyuan Air Quality")

# Main content
if analysis_type == "Mean over 5 Years":
    st.subheader("Mean Pollution Levels over 5 Years")
    mean_pollution_over_5_years = data_df.groupby("year").mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    for pollutant in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]:
        sns.lineplot(x="year", y=pollutant, data=mean_pollution_over_5_years, label=pollutant, marker="o")

    plt.title("Mean Pollution Levels over 5 Years")
    plt.xlabel("Year")
    plt.ylabel("Average Pollution Level")
    plt.legend(title="Pollutant")
    st.pyplot(fig)

elif analysis_type == "Individual Year":
    # Display sample of the dataset for the selected year
    st.subheader(f"Sample of the dataset for {selected_year}:")
    st.write(selected_year_data.head())

    # Display average pollution levels for the selected year
    st.subheader(f"Average Pollution Levels for {selected_year}")
    fig, ax = plt.subplots(figsize=(12, 8))
    for pollutant in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]:
        sns.lineplot(x="month", y=pollutant, data=selected_year_data, label=pollutant, marker="o")
    plt.title(f"Average Pollution Levels for {selected_year}")
    plt.xlabel("Month")
    plt.ylabel("Average Pollution Level")
    plt.legend(title="Pollutant")
    st.pyplot(fig)

    # Display mean temperature and pressure for the selected year
    st.subheader(f"Mean Temperature and Pressure for {selected_year}")
    mean_air_for_year = selected_year_data.groupby("month").agg({"TEMP": "mean", "PRES": "mean"}).reset_index()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    ax[0].plot(mean_air_for_year["month"], mean_air_for_year["TEMP"], marker="o", linewidth=2, color="#39064B")
    ax[0].tick_params(axis="y", labelsize=20)
    ax[0].tick_params(axis="x", labelsize=20, labelrotation=45)
    ax[0].set_ylabel("Temperature (°C)", fontsize=25)
    ax[0].set_title("Mean Temperature", loc="center", fontsize=35)

    ax[1].plot(mean_air_for_year["month"], mean_air_for_year["PRES"], marker="o", linewidth=2, color="#39064B")
    ax[1].tick_params(axis="y", labelsize=20)
    ax[1].tick_params(axis="x", labelsize=20, labelrotation=45)
    ax[1].set_ylabel("Pressure (hPa)", fontsize=25)
    ax[1].set_title("Mean Pressure", loc="center", fontsize=35)

    fig.tight_layout(pad=2.0)
    plt.suptitle(f"Mean Trend of Temperature and Pressure for {selected_year} in Guanyuan", fontsize=45, y=1.05)
    st.pyplot(fig)
