import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    hour_data = pd.read_csv('https://raw.githubusercontent.com/MadeRama21/datasetBikeSharing/refs/heads/main/hour.csv')
    day_data = pd.read_csv('https://raw.githubusercontent.com/MadeRama21/datasetBikeSharing/refs/heads/main/day.csv')
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    return hour_data, day_data
hour_data, day_data = load_data()

season_mapping = {1: "Spring / Musim Semi", 2: "Summer / Musim Panas", 3: "Fall / Musim Gugur", 4: "Winter / Musim Dingin"}
day_data['season'] = day_data['season'].map(season_mapping)
hour_data['season'] = hour_data['season'].map(season_mapping)
st.title("Analisis Data Bike Sharing")
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim", day_data['season'].unique())

filtered_hour_data = hour_data[hour_data['season'] == selected_season]
filtered_day_data = day_data[day_data['season'] == selected_season]

st.subheader("Jawaban Pertanyaan 1: Tren Penggunaan Sepeda Berdasarkan Waktu")

st.write("#### Tren Penggunaan Sepeda Per Jam")
hourly_summary = filtered_hour_data.groupby('hr')['cnt'].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.barh(hourly_summary['hr'], hourly_summary['cnt'])
plt.title("Rata-rata Penggunaan Sepeda Per Jam")
plt.xlabel("Jumlah Penyewaan Sepeda")
plt.ylabel("Jam")
st.pyplot(plt)

st.subheader("Penggunaan Sepeda Berdasarkan Hari Kerja vs Akhir Pekan")
weekday_data = hour_data[hour_data['workingday'] == 1]
weekend_data = hour_data[hour_data['workingday'] == 0]

plt.figure(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=weekday_data, label='Hari Kerja')
sns.lineplot(x='hr', y='cnt', data=weekend_data, label='Akhir Pekan')
plt.title("Tren Penggunaan Sepeda Berdasarkan Jam (Hari Kerja vs Akhir Pekan)")
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.legend()
st.pyplot(plt)

st.subheader("Jawaban Pertanyaan 2: Faktor-Faktor Utama yang Memengaruhi Penyewaan Sepeda Harian")

st.write("#### Hubungan Suhu dengan Jumlah Penyewaan Sepeda")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=filtered_day_data)
plt.title("Hubungan Suhu dengan Jumlah Penyewaan Sepeda")
plt.xlabel("Suhu (Normalisasi)")
plt.ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(plt)

st.write("#### Heatmap Korelasi Antar Variabel")
correlation_matrix = filtered_day_data[['temp', 'hum', 'windspeed', 'cnt']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Heatmap Korelasi Antar Variabel")
st.pyplot(plt)